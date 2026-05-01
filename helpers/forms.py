from django import forms
from django.contrib.auth import get_user_model
from .models import (
    SignupToHelpers, HelperProfile, City, 
    Specialty, Service, Experience, Availability
)

User = get_user_model()

# --- 1. فورم تسجيل المساعد (المرحلة الأولى) ---
class HelperSignupForm(forms.ModelForm):
    first_name = forms.CharField(label="الاسم الأول", widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}))
    last_name = forms.CharField(label="اسم العائلة", widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}))
    email = forms.EmailField(label="البريد الإلكتروني", widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white'}))
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}))

    class Meta:
        model = SignupToHelpers
        fields = ['phone_number', 'national_id', 'moh_authorization', 'training_certificates']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': '05xxxxxxxx'}),
        }

# --- 2. فورم تسجيل الدخول (الذي كان ينقصكِ) ---
class HelperLoginForm(forms.Form):
    email = forms.EmailField(label="البريد الإلكتروني", widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'example@mail.com'}))
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white'}))

# --- 3. فورم ملف المساعد الشخصي ---
class HelperProfileForm(forms.ModelForm):
    class Meta:
        model = HelperProfile
        fields = ['bio', 'city', 'specialty', 'services', 'hourly_rate']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 3, 'placeholder': 'نبذة عن مهاراتك...'}),
            'city': forms.Select(attrs={'class': 'form-select bg-dark text-white'}),
            'specialty': forms.Select(attrs={'class': 'form-select bg-dark text-white'}),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = False
        self.fields['specialty'].required = False
        self.fields['services'].required = False

# --- 4. فورم الخبرة (مطابق للموديل الخاص بكِ) ---
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'years', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'المسمى الوظيفي'}),
            'years': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white', 'placeholder': 'سنوات الخبرة'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 2, 'placeholder': 'وصف مختصر لخبراتك'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

# --- 5. فورم أوقات الإتاحة ---
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select bg-dark text-white'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control bg-dark text-white'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control bg-dark text-white'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False