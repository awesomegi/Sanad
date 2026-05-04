import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Sum, Avg, Q
from django.contrib import messages

from .forms import HelperSignupForm, HelperLoginForm, HelperProfileForm, ExperienceForm, AvailabilityForm
from .models import (
    SignupToHelpers, HelperProfile, City,
    Specialty, Service, Experience, Availability
)

User = get_user_model()


# ─────────────────────────────────────────────
#  Decorator: معتمد فقط
# ─────────────────────────────────────────────

def helper_approved_only(view_func):
    """يتحقق أن المساعد معتمد قبل الدخول لصفحات إدارة البيانات."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_helper_approved:
            return view_func(request, *args, **kwargs)
        return redirect('helpers:wait_review')
    return _wrapped_view


# ─────────────────────────────────────────────
#  1. التسجيل
# ─────────────────────────────────────────────

def signup_helper(request):
    
    if request.method == 'POST':
        form = HelperSignupForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    role='HELPER',  # ✅ هذا السطر الناقص
                    )
                    
                    signup_data = form.save(commit=False)
                    signup_data.user = user
                    signup_data.save()

                    # ✅ الإصلاح: تسجيل دخول المستخدم مباشرة بعد التسجيل
                    auth_login(request, user)

                return redirect('helpers:wait_review')

            except IntegrityError:
                form.add_error('email', 'هذا البريد الإلكتروني مسجل مسبقاً.')
    else:
        form = HelperSignupForm()

    return render(request, 'helpers/signup.html', {'form': form})


# ─────────────────────────────────────────────
#  2. انتظار المراجعة
# ─────────────────────────────────────────────

@login_required
def wait_review(request):
    signup_request = getattr(request.user, 'signup_request', None)
    return render(request, 'helpers/wait_review.html', {
        'signup_request': signup_request
    })


# ─────────────────────────────────────────────
#  3. تسجيل الدخول
# ─────────────────────────────────────────────

def signin_helper(request):
    error_message = None

    if request.method == 'POST':
        form = HelperLoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user     = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f'مرحباً مجدداً، {user.first_name}!')
                return redirect('helpers:helper_dashboard')
            else:
                error_message = 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'
    else:
        form = HelperLoginForm()

    return render(request, 'helpers/signin.html', {
        'form': form,
        'error_message': error_message,
    })


# ─────────────────────────────────────────────
#  4. لوحة التحكم
# ─────────────────────────────────────────────
@login_required
def helper_dashboard(request):
    if not request.user.is_helper_approved:
        return redirect('helpers:wait_review')
    
    helper = getattr(request.user, 'helper_profile', None)
    
    # Real data from bookings
    from bookings.models import Booking
    from django.utils import timezone
    from django.db.models import Sum, Avg
    
    pending_bookings  = []
    active_bookings   = []
    history           = []
    pending_count     = 0
    active_count      = 0
    monthly_earnings  = 0
    rating            = 0

    if helper:
        pending_bookings = list(
            Booking.objects.filter(helper=helper, status='BOOKED')
            .select_related('seeker__user', 'service')
            .order_by('scheduled_date', 'scheduled_start_time')
        )
        active_bookings = list(
            Booking.objects.filter(helper=helper, status='ACTIVE')
            .select_related('seeker__user', 'service')
            .order_by('scheduled_date', 'scheduled_start_time')
        )
        history = list(
            Booking.objects.filter(helper=helper, status__in=['COMPLETED', 'CANCELLED'])
            .select_related('seeker__user', 'service')
            .prefetch_related('seeker_rating')
            .order_by('-scheduled_date', '-scheduled_start_time')[:20]
        )

        pending_count = len(pending_bookings)
        active_count  = len(active_bookings)

        now = timezone.now()
        monthly_earnings = Booking.objects.filter(
            helper=helper,
            status='COMPLETED',
            scheduled_date__month=now.month,
            scheduled_date__year=now.year,
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        rating = Booking.objects.filter(
            helper=helper, status='COMPLETED'
        ).aggregate(avg=Avg('rating__score'))['avg'] or 0

    context = {
        'helper':               helper,
        'is_approved':          request.user.is_helper_approved,
        'pending_count':        pending_count,
        'active_count':         active_count,
        'monthly_earnings':     monthly_earnings,
        'rating':               rating,
        'open_requests':        [],
        'pending_bookings':     pending_bookings,
        'active_bookings':      active_bookings,
        'history':              history,
        'upcoming_bookings':    pending_bookings + active_bookings,
        'unread_notifications': request.user.notifications.filter(is_read=False).count(),
    }
    return render(request, 'helpers/dashboard.html', context)
# ─────────────────────────────────────────────
#  5. Edit profile (approved only)
# ─────────────────────────────────────────────

@login_required
@helper_approved_only
def edit_profile(request):
    profile, _ = HelperProfile.objects.get_or_create(user=request.user)
    experiences    = profile.experiences.all()
    availabilities = profile.availabilities.all()

    if request.method == 'POST':
        form       = HelperProfileForm(request.POST, request.FILES, instance=profile)
        exp_form   = ExperienceForm(request.POST)
        avail_form = AvailabilityForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                updated_profile = form.save(commit=False)

                city_other = request.POST.get('city_other', '').strip()
                if city_other:
                    new_city, _ = City.objects.get_or_create(name=city_other)
                    updated_profile.city = new_city

                spec_other = request.POST.get('specialty_other', '').strip()
                if spec_other:
                    new_spec, _ = Specialty.objects.get_or_create(name=spec_other)
                    updated_profile.specialty = new_spec

                updated_profile.save()
                form.save_m2m()

                if exp_form.is_valid() and exp_form.cleaned_data.get('title'):
                    new_exp = exp_form.save(commit=False)
                    new_exp.helper = profile
                    new_exp.save()

                if avail_form.is_valid() and avail_form.cleaned_data.get('day'):
                    new_avail = avail_form.save(commit=False)
                    new_avail.helper = profile
                    new_avail.save()

                updated_profile.services.clear()
                if updated_profile.specialty:
                    for s_name in request.POST.getlist('manual_services[]'):
                        if s_name.strip():
                            unique_code = f"{slugify(s_name)}_{secrets.token_hex(3)}"
                            service, _ = Service.objects.get_or_create(
                                name=s_name,
                                specialty=updated_profile.specialty,
                                defaults={'code': unique_code}
                            )
                            updated_profile.services.add(service)
                else:
                    messages.warning(request, 'يرجى اختيار التخصص أولاً لحفظ الخدمات.')

            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح.')
            return redirect('helpers:helper_dashboard')

    else:
        form       = HelperProfileForm(instance=profile)
        exp_form   = ExperienceForm()
        avail_form = AvailabilityForm()

    return render(request, 'helpers/edit_profile.html', {
        'form':           form,
        'exp_form':       exp_form,
        'avail_form':     avail_form,
        'profile':        profile,
        'experiences':    experiences,
        'availabilities': availabilities,
        'cities':         City.objects.all(),
        'specialties':    Specialty.objects.all(),
    })


# ─────────────────────────────────────────────
#  6. حذف خبرة / موعد توفر
# ─────────────────────────────────────────────

@login_required
@helper_approved_only
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, helper__user=request.user)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'تم حذف الخبرة.')
    return redirect('helpers:edit_profile')


@login_required
@helper_approved_only
def delete_availability(request, pk):
    slot = get_object_or_404(Availability, pk=pk, helper__user=request.user)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, 'تم حذف وقت التوفر.')
    return redirect('helpers:edit_profile')


# ─────────────────────────────────────────────
#  7. قائمة المساعدين (عامة)
# ─────────────────────────────────────────────

def helper_list(request):
    helpers = HelperProfile.objects.filter(
        is_active=True,
        verification_status='APPROVED'
    ).select_related('user', 'city', 'specialty').prefetch_related('services')

    service_id = request.GET.get('service')
    city_id    = request.GET.get('city')
    max_rate   = request.GET.get('max_rate')
    min_rating = request.GET.get('min_rating')
    query      = request.GET.get('q')

    if service_id:
        helpers = helpers.filter(services__id=service_id)
    if city_id:
        helpers = helpers.filter(city__id=city_id)
    if max_rate:
        helpers = helpers.filter(hourly_rate__lte=max_rate)
    if query:
        helpers = helpers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)  |
            Q(bio__icontains=query)
        )

    helpers = helpers.annotate(avg_rating=Avg('orders__rating'))

    if min_rating:
        helpers = helpers.filter(avg_rating__gte=min_rating)

    recommended_ids = set()
    if request.user.is_authenticated and hasattr(request.user, 'seekerprofile'):
        seeker_category = request.user.seekerprofile.disability_category
        recommended_ids = set(
            helpers.filter(specialty__name__iexact=seeker_category)
                   .values_list('id', flat=True)
        )

    return render(request, 'helpers/helper_list.html', {
        'helpers':          helpers,
        'recommended_ids':  recommended_ids,
        'services':         Service.objects.all(),
        'cities':           City.objects.all(),
        'selected_service': service_id,
        'selected_city':    city_id,
        'max_rate':         max_rate,
        'min_rating':       min_rating,
        'query':            query,
    })


# ─────────────────────────────────────────────
#  8. ملف المساعد (عام)
# ─────────────────────────────────────────────

def helper_detail(request, pk):
    helper = get_object_or_404(
        HelperProfile.objects.select_related('user', 'city', 'specialty')
                             .prefetch_related('services', 'availabilities'),
        pk=pk,
        is_active=True,
        verification_status='APPROVED'
    )

    avg_rating      = helper.orders.aggregate(avg=Avg('rating'))['avg'] if hasattr(helper, 'orders') else None
    completed_count = helper.orders.filter(status='COMPLETED').count() if hasattr(helper, 'orders') else 0
    availability    = helper.availabilities.filter(is_active=True).order_by('day')

    return render(request, 'helpers/helper_detail.html', {
        'helper':          helper,
        'avg_rating':      avg_rating,
        'completed_count': completed_count,
        'availability':    availability,
    })

# ─────────────────────────────────────────────
#  9. إدارة الحجوزات (للمساعد)
# ─────────────────────────────────────────────

@login_required
@helper_approved_only
def accept_booking(request, booking_id):
    """Helper accepts a BOOKED booking → ACTIVE, notifies seeker."""
    if request.method != 'POST':
        return redirect('helpers:helper_dashboard')

    from bookings.models import Booking
    from notifications.services import notify_seeker_booking_accepted

    helper  = get_object_or_404(HelperProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id, helper=helper, status='BOOKED')

    booking.status = 'ACTIVE'
    booking.save()

    notify_seeker_booking_accepted(booking)

    messages.success(request, 'تم قبول الحجز وإشعار الباحث.')
    return redirect('helpers:helper_dashboard')


@login_required
@helper_approved_only
def cancel_booking_by_helper(request, booking_id):
    """Helper cancels a BOOKED/ACTIVE booking → CANCELLED + refund + notify seeker."""
    if request.method != 'POST':
        return redirect('helpers:helper_dashboard')

    import os
    import requests as http_requests
    from django.utils import timezone
    from bookings.models import Booking
    from payments.models import Payment
    from notifications.services import (
        notify_seeker_booking_cancelled_by_helper,
        notify_seeker_refund_processed,
    )

    helper  = get_object_or_404(HelperProfile, user=request.user)
    booking = get_object_or_404(
        Booking, pk=booking_id, helper=helper, status__in=['BOOKED', 'ACTIVE']
    )

    payment = getattr(booking, 'payment', None)

    if payment and payment.status == Payment.Status.PAID:
        if payment.transaction_id.startswith('FAKE-'):
            refund_ok = True
        else:
            secret_key = os.environ.get('MOYASAR_SECRET_KEY')
            resp       = http_requests.post(
                f'https://api.moyasar.com/v1/payments/{payment.transaction_id}/refund',
                auth=(secret_key, ''),
            )
            refund_ok = (resp.status_code == 200)

        if not refund_ok:
            messages.error(request, 'فشل معالجة الاسترداد. يرجى التواصل مع الدعم.')
            return redirect('helpers:helper_dashboard')

        payment.status      = Payment.Status.REFUNDED
        payment.refunded_at = timezone.now()
        payment.save()
        notify_seeker_refund_processed(booking)

    booking.status = 'CANCELLED'
    booking.save()

    notify_seeker_booking_cancelled_by_helper(booking)

    messages.success(request, 'تم إلغاء الحجز وإشعار الباحث.')
    return redirect('helpers:helper_dashboard')


@login_required
@helper_approved_only
def complete_booking(request, booking_id):
    """Helper marks an ACTIVE booking as COMPLETED, notifies seeker."""
    if request.method != 'POST':
        return redirect('helpers:helper_dashboard')

    from bookings.models import Booking
    from notifications.services import notify_seeker_booking_completed

    helper  = get_object_or_404(HelperProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id, helper=helper, status='ACTIVE')

    booking.status = 'COMPLETED'
    booking.save()

    notify_seeker_booking_completed(booking)

    messages.success(request, 'تم تأكيد إتمام الجلسة.')
    return redirect('helpers:helper_dashboard')


@login_required
@helper_approved_only
def rate_seeker(request, booking_id):
    """Helper rates the seeker after a COMPLETED session."""
    from bookings.models import Booking, SeekerRating

    helper  = get_object_or_404(HelperProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id, helper=helper, status='COMPLETED')

    if hasattr(booking, 'seeker_rating'):
        messages.info(request, 'لقد قيّمت هذا الباحث مسبقاً.')
        return redirect('helpers:helper_dashboard')

    if request.method == 'POST':
        score   = request.POST.get('score')
        comment = request.POST.get('comment', '')

        if score and score.isdigit() and 1 <= int(score) <= 5:
            SeekerRating.objects.create(
                booking=booking,
                score=int(score),
                comment=comment,
            )
            messages.success(request, 'شكراً! تم إرسال تقييمك بنجاح.')
            return redirect('helpers:helper_dashboard')
        else:
            messages.error(request, 'يرجى اختيار تقييم صحيح من 1 إلى 5.')

    return render(request, 'helpers/rate_seeker.html', {'booking': booking})