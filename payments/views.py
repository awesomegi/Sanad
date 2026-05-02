from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment


@login_required
def checkout(request, booking_id):
    if not request.user.is_seeker:
        return redirect('home')

    # TODO: When Rimas's Booking model is ready, replace this mock data
    # with: booking = get_object_or_404(Booking, id=booking_id, seeker=request.user)
    booking = {
        'id': booking_id,
        'service_name': 'Grocery shopping at Panda',
        'helper_name': 'Rimas Al-Shahrani',
        'helper_initials': 'RS',
        'helper_rating': 4.8,
        'helper_completed': 47,
        'scheduled_date': 'Mon Jan 15',
        'scheduled_time': '6:00 PM',
        'hourly_rate': 50,
        'hours': 2.0,
        'total': 100,
    }

    return render(request, 'payments/checkout.html', {'booking': booking})


@login_required
def payment_success(request, booking_id):
    return render(request, 'payments/success.html', {'booking_id': booking_id})


@login_required
def payment_failed(request, booking_id):
    return render(request, 'payments/failed.html', {'booking_id': booking_id})


@login_required
def fake_pay(request, booking_id):
    """
    Temporary view — fakes a successful payment for now.
    Will be replaced by Moyasar integration in the next step.
    """
    if request.method != 'POST':
        return redirect('checkout', booking_id=booking_id)

    # TODO: Replace with real Moyasar integration
    messages.success(request, 'Payment processed successfully!')
    return redirect('payment_success', booking_id=booking_id)
