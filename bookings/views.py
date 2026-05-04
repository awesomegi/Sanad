from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from helpers.models import HelperProfile, City, Specialty
from .models import Booking, Rating
from notifications.services import notify_booking_confirmed, notify_booking_cancelled, notify_rating_received


# ── Decorator: Seeker فقط ──────────────────
def seeker_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seeker:
            return view_func(request, *args, **kwargs)
        return redirect('home')
    return _wrapped_view


# ── 1. قائمة المساعدين ─────────────────────
@login_required
@seeker_only
def helpers_list(request):
    helpers = HelperProfile.objects.filter(
        is_active=True,
        verification_status='APPROVED'
    ).select_related('user', 'city', 'specialty').prefetch_related('services', 'experiences')

    query              = request.GET.get('q')
    selected_city      = request.GET.get('city')
    selected_specialty = request.GET.get('specialty')
    max_rate           = request.GET.get('max_rate')

    if query:
        helpers = helpers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    if selected_city:
        helpers = helpers.filter(city__id=selected_city)
    if selected_specialty:
        helpers = helpers.filter(specialty__id=selected_specialty)
    if max_rate:
        helpers = helpers.filter(hourly_rate__lte=max_rate)

    helpers = helpers.annotate(avg_rating=Avg('orders__rating__score'))

    context = {
        'helpers':            helpers,
        'cities':             City.objects.all(),
        'specialties':        Specialty.objects.all(),
        'query':              query,
        'selected_city':      selected_city,
        'selected_specialty': selected_specialty,
        'max_rate':           max_rate,
    }
    return render(request, 'bookings/helpers_list.html', context)


# ── 2. حجز مساعد ─────────────────────────
@login_required
@seeker_only
def book_helper(request, pk):
    helper = get_object_or_404(
        HelperProfile,
        pk=pk,
        is_active=True,
        verification_status='APPROVED'
    )

    if request.method == 'POST':
        service_id           = request.POST.get('service')
        scheduled_date       = request.POST.get('scheduled_date')
        scheduled_start_time = request.POST.get('scheduled_start_time')
        hours                = request.POST.get('hours')
        notes                = request.POST.get('notes', '')

        if not all([service_id, scheduled_date, scheduled_start_time, hours]):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            return render(request, 'bookings/book_helper.html', {'helper': helper})

        try:
            service = helper.services.get(id=service_id)
        except Exception:
            messages.error(request, 'الخدمة المختارة غير صحيحة.')
            return render(request, 'bookings/book_helper.html', {'helper': helper})

        booking = Booking.objects.create(
            seeker               = request.user.seeker_profile,
            helper               = helper,
            service              = service,
            scheduled_date       = scheduled_date,
            scheduled_start_time = scheduled_start_time,
            hours                = hours,
            notes                = notes,
            total_amount         = 0,  # overwritten by model.save()
        )

        return redirect('payments:checkout', booking_id=booking.id)

    return render(request, 'bookings/book_helper.html', {'helper': helper})


# ── 3. بروفايل المساعد ─────────────────────
@login_required
@seeker_only
def helper_detail(request, pk):
    helper = get_object_or_404(
        HelperProfile.objects.select_related('user', 'city', 'specialty')
                             .prefetch_related('services', 'experiences', 'availabilities'),
        pk=pk,
        is_active=True,
        verification_status='APPROVED'
    )

    avg_rating = helper.orders.aggregate(avg=Avg('rating__score'))['avg']
    completed_count = helper.orders.filter(status='COMPLETED').count() if hasattr(helper, 'orders') else 0
    availability    = helper.availabilities.filter(is_active=True).order_by('day')

    context = {
        'helper':          helper,
        'avg_rating':      avg_rating,
        'completed_count': completed_count,
        'availability':    availability,
    }
    return render(request, 'bookings/helper_detail.html', context)


# ── 3. تقييم المساعد ─────────────────────
@login_required
@seeker_only
def rate_helper(request, booking_id):
    seeker  = request.user.seeker_profile
    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        seeker=seeker,
        status='COMPLETED'
    )

    # تأكد ما قيّم قبل
    if hasattr(booking, 'rating'):
        return redirect('seeker_dashboard')

    if request.method == 'POST':
        score   = request.POST.get('score')
        comment = request.POST.get('comment', '')

        if score and score.isdigit() and 1 <= int(score) <= 5:
            Rating.objects.create(
                booking=booking,
                score=int(score),
                comment=comment
            )
            
            notify_rating_received(booking)

            return redirect('seeker_dashboard')

    return render(request, 'bookings/rate_helper.html', {'booking': booking})

