from django import forms
from django.contrib.auth import get_user_model
from .models import (
    SignupToHelpers, HelperProfile, City, 
    Specialty, Service, Experience, Availability
)

User = get_user_model()

# --- 1. Helper Signup Form ---
class HelperSignupForm(forms.ModelForm):
    first_name = forms.CharField(label="الاسم الأول", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(label="اسم العائلة", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email      = forms.EmailField(label="البريد الإلكتروني", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password   = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model  = SignupToHelpers
        fields = ['phone_number', 'national_id', 'moh_authorization', 'training_certificates']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05xxxxxxxx'}),
        }

# --- 2. Helper Login Form ---
class HelperLoginForm(forms.Form):
    email    = forms.EmailField(label="البريد الإلكتروني", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}))
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# --- 3. Helper Profile Form ---
class HelperProfileForm(forms.ModelForm):
    class Meta:
        model  = HelperProfile
        fields = ['bio', 'profile_photo', 'city', 'specialty', 'services', 'hourly_rate']
        widgets = {
            'bio':           forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'نبذة عن مهاراتك...'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'city':          forms.Select(attrs={'class': 'form-select'}),
            'specialty':     forms.Select(attrs={'class': 'form-select'}),
            'services':      forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'hourly_rate':   forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required      = False
        self.fields['specialty'].required = False
        self.fields['services'].required  = False

# --- 4. Experience Form ---
class ExperienceForm(forms.ModelForm):
    class Meta:
        model  = Experience
        fields = ['title', 'years', 'description']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'المسمى الوظيفي'}),
            'years':       forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سنوات الخبرة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'وصف مختصر لخبراتك'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

# --- 5. Availability Form ---
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model  = Availability
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day':        forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False