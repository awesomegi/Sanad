from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import User, SeekerProfile


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
        return redirect('home')

    return render(request, 'accounts/signup_seeker.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')


