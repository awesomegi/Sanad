from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from bookings.models import Booking


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

    return render(request, 'payments/checkout.html', {'booking': booking})


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, seeker=request.user.seeker_profile)
    return render(request, 'payments/success.html', {'booking': booking})


@login_required
def payment_failed(request, booking_id):
    return render(request, 'payments/failed.html', {'booking_id': booking_id})


@login_required
def fake_pay(request, booking_id):
    """
    Temporary view — fakes a successful payment.
    Will be replaced by Moyasar integration in the next step.
    """
    if request.method != 'POST':
        return redirect('payments:checkout', booking_id=booking_id)

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        seeker=request.user.seeker_profile,
    )

    # Create the Payment record
    Payment.objects.create(
        booking=booking,
        seeker=request.user,
        helper=booking.helper,
        amount=booking.total_amount,
        status=Payment.PaymentStatus.PAID,
        transaction_id=f'FAKE-{booking.id}-{int(timezone.now().timestamp())}',
        payment_method=Payment.PaymentMethod.MADA,
        paid_at=timezone.now(),
    )

    messages.success(request, 'Payment processed successfully!')
    return redirect('payments:payment_success', booking_id=booking_id)