from .models import Notification


# ── Helper receives new booking request ──────────────────────────────────────
def notify_new_booking(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.BOOKING_CONFIRMED,
        message = (
            f"لديك طلب حجز جديد من {booking.seeker.user.get_full_name()} "
            f"بتاريخ {booking.scheduled_date}. "
            f"يرجى قبول الطلب أو رفضه من لوحة التحكم."
        ),
    )


# ── Seeker: payment received, awaiting helper confirmation ───────────────────
def notify_seeker_payment_success(booking):
    Notification.objects.create(
        user    = booking.seeker.user,
        type    = Notification.Type.PAYMENT_SUCCESS,
        message = (
            f"تم استلام دفعتك بنجاح ({booking.total_amount} ر.س). "
            f"بانتظار تأكيد المساعد {booking.helper.user.get_full_name()}."
        ),
    )


# ── Seeker: helper accepted the booking ─────────────────────────────────────
def notify_seeker_booking_accepted(booking):
    Notification.objects.create(
        user    = booking.seeker.user,
        type    = Notification.Type.BOOKING_ACCEPTED,
        message = (
            f"قبل المساعد {booking.helper.user.get_full_name()} حجزك "
            f"بتاريخ {booking.scheduled_date} الساعة {booking.scheduled_start_time}."
        ),
    )


# ── Seeker: helper cancelled the booking ─────────────────────────────────────
def notify_seeker_booking_cancelled_by_helper(booking):
    Notification.objects.create(
        user    = booking.seeker.user,
        type    = Notification.Type.BOOKING_CANCELLED,
        message = (
            f"أُلغي حجزك مع {booking.helper.user.get_full_name()} "
            f"بتاريخ {booking.scheduled_date} من قِبَل المساعد. "
            f"سيتم رد المبلغ خلال 3–5 أيام عمل."
        ),
    )


# ── Helper: seeker cancelled the booking ─────────────────────────────────────
def notify_helper_booking_cancelled_by_seeker(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.BOOKING_CANCELLED,
        message = (
            f"ألغى {booking.seeker.user.get_full_name()} حجزه "
            f"بتاريخ {booking.scheduled_date}."
        ),
    )


# ── Seeker: session marked complete by helper ────────────────────────────────
def notify_seeker_booking_completed(booking):
    Notification.objects.create(
        user    = booking.seeker.user,
        type    = Notification.Type.BOOKING_COMPLETED,
        message = (
            f"تم إتمام جلستك مع {booking.helper.user.get_full_name()} بنجاح. "
            f"شاركنا رأيك بتقييم المساعد!"
        ),
    )


# ── Seeker: refund processed ─────────────────────────────────────────────────
def notify_seeker_refund_processed(booking):
    Notification.objects.create(
        user    = booking.seeker.user,
        type    = Notification.Type.REFUND_PROCESSED,
        message = (
            f"تم رد مبلغ {booking.total_amount} ر.س للحجز "
            f"بتاريخ {booking.scheduled_date}."
        ),
    )


# ── Helper: received a rating ────────────────────────────────────────────────
def notify_rating_received(booking):
    Notification.objects.create(
        user    = booking.helper.user,
        type    = Notification.Type.RATING_RECEIVED,
        message = f"لقد تلقيت تقييماً جديداً من {booking.seeker.user.get_full_name()}.",
    )


# ── Backward-compat aliases (used in bookings/views.py imports) ───────────────
def notify_booking_confirmed(booking):
    notify_new_booking(booking)


def notify_booking_cancelled(booking):
    notify_helper_booking_cancelled_by_seeker(booking)
