from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, SeekerProfile
from django.db import models


@login_required
def seeker_dashboard(request):
    if not request.user.is_seeker:
        return redirect('home')

    seeker = request.user.seeker_profile

    # Pull all bookings for this seeker
    all_bookings = seeker.bookings.select_related(
        'helper__user',
        'service',
    ).order_by('-scheduled_date', '-scheduled_start_time')

    # Active = BOOKED or ACTIVE
    active_bookings = all_bookings.filter(status__in=['BOOKED', 'ACTIVE'])

    # History = COMPLETED or CANCELLED
    history = all_bookings.filter(status__in=['COMPLETED', 'CANCELLED'])

    # Stats
    active_count = active_bookings.count()
    completed_count = all_bookings.filter(status='COMPLETED').count()

    # Total spent = sum of total_amount across all PAID payments
    from payments.models import Payment
    total_spent = Payment.objects.filter(
        seeker=request.user,
        status='PAID',
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    context = {
        'seeker': seeker,
        'active_count': active_count,
        'completed_count': completed_count,
        'total_spent': total_spent,
        'active_bookings': active_bookings,
        'history': history,
    }

    return render(request, 'accounts/seeker_dashboard.html', context)


def signup_seeker(request):
    if request.method == 'POST':
        # Read all form fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        disability_type = request.POST.get('disability_type')
        disability_category = request.POST.get('disability_category')
        address = request.POST.get('address')
        emergency_contact = request.POST.get('emergency_contact')

        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup_seeker.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists')
            return render(request, 'accounts/signup_seeker.html')

        # Create the User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=User.Role.SEEKER,
        )

        # Create the SeekerProfile
        SeekerProfile.objects.create(
            user=user,
            disability_type=disability_type,
            disability_category=disability_category,
            address=address,
            emergency_contact=emergency_contact,
        )

        # Log them in immediately
        login(request, user)
        messages.success(request, f'Welcome to Sanad, {first_name}!')
        return redirect('seeker_dashboard')

    return render(request, 'accounts/signup_seeker.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_seeker:
                return redirect('seeker_dashboard')  
            elif user.is_helper:
                return redirect('helpers:helper_dashboard')
        return redirect('home')
        
    else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('home')


