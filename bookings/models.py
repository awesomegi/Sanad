from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from helpers.models import HelperProfile, Service

# Instructor-approved field naming convention:
# booking.service.name (string)
# booking.scheduled_date (date)
# booking.scheduled_start_time (time)
# booking.hours (decimal)
# booking.total_amount (decimal)
# booking.helper.user.first_name


class Booking(models.Model):

    class Status(models.TextChoices):
        BOOKED    = 'BOOKED',    'Booked'
        ACTIVE    = 'ACTIVE',    'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # Users
    seeker = models.ForeignKey(
        'accounts.SeekerProfile',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    helper = models.ForeignKey(
        HelperProfile,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # Booking details
    service              = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    scheduled_date       = models.DateField()
    scheduled_start_time = models.TimeField()
    hours                = models.DecimalField(max_digits=4, decimal_places=1)
    notes                = models.TextField(blank=True)

    # Payment
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    # Status
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_start_time']

    def __str__(self):
        return f"{self.seeker.user.get_full_name()} → {self.helper.user.get_full_name()} | {self.scheduled_date}"

    def save(self, *args, **kwargs):
        # Auto-calculate total amount
        if self.helper.hourly_rate and self.hours:
            self.total_amount = self.helper.hourly_rate * Decimal(str(self.hours))
        super().save(*args, **kwargs)


class Rating(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.seeker.user.get_full_name()} → {self.score}⭐"