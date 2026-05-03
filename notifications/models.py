from django.db import models
from django.conf import settings


class Notification(models.Model):

    class Type(models.TextChoices):
        BOOKING_CONFIRMED = 'BOOKING_CONFIRMED', 'Booking Confirmed'
        BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Booking Cancelled'
        PAYMENT_SUCCESS   = 'PAYMENT_SUCCESS',   'Payment Success'
        PAYMENT_FAILED    = 'PAYMENT_FAILED',     'Payment Failed'
        RATING_RECEIVED   = 'RATING_RECEIVED',   'Rating Received'

    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type       = models.CharField(max_length=30, choices=Type.choices)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.type}"