from django.db import models
from django.conf import settings


class Notification(models.Model):

    class Type(models.TextChoices):
        BOOKING_CONFIRMED = 'BOOKING_CONFIRMED', 'Booking Confirmed'       # helper: new booking arrived
        BOOKING_ACCEPTED  = 'BOOKING_ACCEPTED',  'Booking Accepted'        # seeker: helper confirmed
        BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Booking Cancelled'       # both parties
        BOOKING_COMPLETED = 'BOOKING_COMPLETED', 'Booking Completed'       # seeker: session done
        PAYMENT_SUCCESS   = 'PAYMENT_SUCCESS',   'Payment Success'         # seeker: payment received
        PAYMENT_FAILED    = 'PAYMENT_FAILED',    'Payment Failed'          # seeker: payment failed
        REFUND_PROCESSED  = 'REFUND_PROCESSED',  'Refund Processed'        # seeker: money returned
        RATING_RECEIVED   = 'RATING_RECEIVED',   'Rating Received'         # helper: got rated

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