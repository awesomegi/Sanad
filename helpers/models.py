from django.db import models
from django.conf import settings
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True) 
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.specialty.name} - {self.name}"
    
class HelperProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    bio = models.TextField(max_length=500, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(Service)
    
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}"

class Availability(models.Model):
    class Days(models.TextChoices):
        SUNDAY = 'SUN', 'Sunday'
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'

    helper = models.ForeignKey(HelperProfile, on_delete=models.CASCADE)
    
    day = models.CharField(max_length=3, choices=Days.choices)
    start_time = models.TimeField() 
    end_time = models.TimeField()   
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.helper.user.email} - {self.day} ({self.start_time} to {self.end_time})"
    
class Experience(models.Model):
    helper = models.ForeignKey(HelperProfile, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    years = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title