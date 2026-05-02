from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import SignupToHelpers, City, Specialty, Service, HelperProfile, Availability, Experience

@admin.register(SignupToHelpers)
class SignupToHelpersAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'phone_number', 'status', 'view_docs', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number')
    actions = ['approve_helpers', 'reject_helpers']

    @admin.action(description="Approve selected helper applications")
    def approve_helpers(self, request, queryset):
        for signup_entry in queryset:
            signup_entry.status = 'APPROVED'
            signup_entry.save()

            profile, created = HelperProfile.objects.get_or_create(
                user=signup_entry.user,
                defaults={'verification_status': 'APPROVED'}
            )
            if not created:
                profile.verification_status = 'APPROVED'
                profile.save()

        self.message_user(request, f"تم اعتماد {queryset.count()} طلب بنجاح.")

    @admin.action(description="Reject selected helper applications")
    def reject_helpers(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f"Successfully rejected {updated} applications.")

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def view_docs(self, obj):
        html = ""
        if obj.national_id:
            html += f'<a href="{obj.national_id.url}" target="_blank" style="color: #d4af37; font-weight:bold; margin-right:15px;">ID View</a>'
        if obj.moh_authorization:
            html += f'<a href="{obj.moh_authorization.url}" target="_blank" style="color: #d4af37; font-weight:bold;">MOH Auth</a>'
        return mark_safe(html) if html else "No Docs"
    view_docs.short_description = "Verification Documents"


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0
    classes = ('collapse',)

@admin.register(HelperProfile)
class HelperProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'specialty', 'city', 'hourly_rate', 'is_active', 'verification_status')
    list_editable = ('is_active', 'hourly_rate')
    list_filter = ('specialty', 'city', 'is_active', 'created_at')
    search_fields = ('user__email', 'specialty__name', 'bio')
    filter_horizontal = ('services',)

    fieldsets = (
        ('General Information', {
            'fields': ('user', 'city', 'bio', 'verification_status'),
            'description': 'البيانات الشخصية والموقع الجغرافي للمساعد المعتمد'
        }),
        ('Professional Details', {
            'fields': ('specialty', 'services', 'hourly_rate', 'is_active'),
            'classes': ('wide',),
        }),
    )

    inlines = [ExperienceInline, AvailabilityInline]

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Helper Email'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'code')
    search_fields = ('name', 'code')
    list_filter = ('specialty',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)