import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from bookings.models import Booking
from django.contrib.auth.decorators import login_required
import requests




@login_required
def checkout(request, booking_id):
    if not request.user.is_seeker:
        return redirect('home')

    # Fetch real booking — only if it belongs to this seeker
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )
    context = {
        'booking': booking,
        'moyasar_publishable_key' : os.getenv('MOYASAR_PUBLISHABLE_KEY'),
        'amount_in_halalas': int(booking.total_amount * 100),  # Convert to halalas
    }

    return render(request, 'payments/checkout.html', context)


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, seeker=request.user.seeker_profile)
    return render(request, 'payments/success.html', {'booking': booking})


@login_required
def payment_failed(request, booking_id):
    return render(request, 'payments/failed.html', {'booking_id': booking_id})


@login_required
def fake_pay(request, booking_id):
    """Kept as fallback safety net — useful if Moyasar fails during demo."""
    if request.method != 'POST':
        return redirect('payments:checkout', booking_id=booking_id)

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )

    Payment.objects.update_or_create(
    booking=booking,
    defaults={
        'seeker': request.user,
        'helper': booking.helper,
        'amount': booking.total_amount,
        'status': Payment.Status.PAID,
        'transaction_id': f'FAKE-{booking.id}-{int(timezone.now().timestamp())}',
        'payment_method': Payment.PaymentMethod.MADA,
        'paid_at': timezone.now(),
    }
)

    messages.success(request, 'Payment processed successfully!')
    return redirect('payments:payment_success', booking_id=booking_id)


@login_required
def moyasar_callback(request):
    payment_id = request.GET.get('id')
    booking_id = request.GET.get('booking_id')

    if not payment_id or not booking_id:
        messages.error(request, 'Missing payment information.')
        return redirect('home')

    secret_key = os.environ.get('MOYASAR_SECRET_KEY')
    response = requests.get(
        f'https://api.moyasar.com/v1/payments/{payment_id}',
        auth=(secret_key, ''),
    )

    if response.status_code != 200:
        messages.error(request, 'Could not verify payment with Moyasar.')
        return redirect('payments:payment_failed', booking_id=booking_id)

    moyasar_data = response.json()
    status = moyasar_data.get('status')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )

    if status == 'paid':
        source_type = moyasar_data.get('source', {}).get('type', '').upper()
        payment_method_map = {
            'CREDITCARD': Payment.PaymentMethod.VISA,
            'APPLEPAY': Payment.PaymentMethod.APPLE_PAY,
        }
        payment_method = payment_method_map.get(source_type, Payment.PaymentMethod.MADA)

        Payment.objects.update_or_create(
            booking=booking,
            defaults={
                'seeker': request.user,
                'helper': booking.helper,
                'amount': booking.total_amount,
                'status': Payment.Status.PAID,
                'transaction_id': payment_id,
                'payment_method': payment_method,
                'paid_at': timezone.now(),
            }
        )

        messages.success(request, 'Payment confirmed!')
        return redirect('payments:payment_success', booking_id=booking_id)

    elif status == 'failed':
        messages.error(request, 'Payment was declined.')
        return redirect('payments:payment_failed', booking_id=booking_id)

    else:
        messages.error(request, f'Unexpected payment status: {status}')
        return redirect('payments:payment_failed', booking_id=booking_id)


@login_required
def refund_confirm(request, booking_id):
    if not request.user.is_seeker:
        return redirect('home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )

    if booking.status not in ['BOOKED', 'ACTIVE']:
        messages.error(request, 'لا يمكن إلغاء هذا الحجز.')
        return redirect('seeker_dashboard')

    payment = getattr(booking, 'payment', None)

    return render(request, 'payments/refund_confirm.html', {
        'booking': booking,
        'payment': payment,
    })


@login_required
def process_refund(request, booking_id):
    """
    Processes a refund: calls Moyasar refund API, updates Payment + Booking status.
    Only accepts POST.
    """
    if request.method != 'POST':
        return redirect('payments:refund_confirm', booking_id=booking_id)

    if not request.user.is_seeker:
        return redirect('home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )

    # Only active bookings can be cancelled
    if booking.status not in ['BOOKED', 'ACTIVE']:
        messages.error(request, 'لا يمكن إلغاء هذا الحجز.')
        return redirect('seeker_dashboard')

    # Get the Payment record
    payment = getattr(booking, 'payment', None)
    if not payment:
        messages.error(request, 'لم يتم العثور على سجل الدفع.')
        return redirect('seeker_dashboard')

    if payment.status != Payment.Status.PAID:
        messages.error(request, 'لا يمكن استرداد دفعة غير مكتملة.')
        return redirect('seeker_dashboard')

    # Call Moyasar refund API (skip for FAKE payments)
    if payment.transaction_id.startswith('FAKE-'):
        # Fake payment — just mark as refunded without calling Moyasar
        refund_succeeded = True
    else:
        secret_key = os.environ.get('MOYASAR_SECRET_KEY')
        response = requests.post(
            f'https://api.moyasar.com/v1/payments/{payment.transaction_id}/refund',
            auth=(secret_key, ''),
        )
        refund_succeeded = (response.status_code == 200)

        if not refund_succeeded:
            messages.error(request, 'فشل الاسترداد. يرجى التواصل مع الدعم.')
            return redirect('payments:refund_confirm', booking_id=booking_id)

    # Update Payment status
    payment.status = Payment.Status.REFUNDED
    payment.refunded_at = timezone.now()
    payment.save()

    # Update Booking status
    booking.status = 'CANCELLED'
    booking.save()

    messages.success(request, 'تم إلغاء الحجز واسترداد المبلغ بنجاح.')
    return redirect('payments:refund_success', booking_id=booking_id)


@login_required
def refund_success(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )
    return render(request, 'payments/refund_success.html', {'booking': booking})