from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SEEKER = 'SEEKER', 'Seeker'
        HELPER = 'HELPER', 'Helper'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    


class SeekerProfile(models.Model):
    
    class DisabilityType(models.TextChoices):
        PERMANENT = 'PERMANENT', 'Permanent'
        TEMPORARY = 'TEMPORARY', 'Temporary'

    class DisabilityCategory(models.TextChoices):
        MOBILITY = 'MOBILITY', 'Mobility'
        VISUAL = 'VISUAL', 'Visual'
        HEARING = 'HEARING', 'Hearing'
        COGNITIVE = 'COGNITIVE', 'Cognitive'    
        TEMPORARY_INJURY = 'TEMPORARY_INJURY', 'Temporary Injury'
        OTHER = 'OTHER', 'Other'

    user = models.OneToOneField(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='seeker_profile'
    )
    disability_type = models.CharField(
        max_length=20, 
        choices=DisabilityType.choices
    )
    disability_category = models.CharField(
        max_length=20, 
        choices=DisabilityCategory.choices
    )
    address = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Seeker)"