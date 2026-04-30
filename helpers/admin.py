from django.contrib import admin
from .models import City, Specialty, Service, HelperProfile, Availability, Experience

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1 
    fields = ('title', 'years', 'description') 

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0 
    classes = ('collapse',) 

@admin.register(HelperProfile)
class HelperProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'specialty', 'city', 'hourly_rate', 'is_active')
    
    list_editable = ('is_active', 'hourly_rate') 
    
    list_filter = ('specialty', 'city', 'is_active', 'created_at')
    
    search_fields = ('user__email', 'specialty__name', 'bio')
    
    fieldsets = (
        ('General Information', {
            'fields': ('user', 'city', 'bio'),
            'description': 'بيانات المساعد الشخصية والموقع الجغرافي'
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

admin.site.register(City)
admin.site.register(Specialty)