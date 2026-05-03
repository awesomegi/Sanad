from django.contrib import admin
from .models import Booking, Rating


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = ('id', 'seeker', 'helper', 'service', 'scheduled_date', 'scheduled_start_time', 'total_amount', 'status')
    list_filter     = ('status', 'scheduled_date')
    search_fields   = ('seeker__user__email', 'helper__user__email')
    readonly_fields = ('total_amount', 'created_at', 'updated_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'score', 'created_at')
    list_filter  = ('score',)