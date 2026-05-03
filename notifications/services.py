from .models import Notification


def notify_booking_confirmed(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.BOOKING_CONFIRMED,
        message = f"لديك حجز جديد من {booking.seeker.user.get_full_name()} بتاريخ {booking.scheduled_date}."
    )


def notify_booking_cancelled(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.BOOKING_CANCELLED,
        message = f"تم إلغاء الحجز من {booking.seeker.user.get_full_name()} بتاريخ {booking.scheduled_date}."
    )


def notify_rating_received(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.RATING_RECEIVED,
        message = f"لقد تلقيت تقييماً جديداً من {booking.seeker.user.get_full_name()}."
    )