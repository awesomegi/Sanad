from django.db import models
from django.conf import settings



# 1. جداول التصنيفات (المدن والتخصصات)
class City(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name
    
class Specialty(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name

# 2. نموذج طلب الانضمام (المرحلة الأولى - قبل الاعتماد)
# في ملف helpers/models.py

class SignupToHelpers(models.Model):
    # يفضل دائماً استخدام اللغة الإنجليزية للقيم المخزنة (اليسار) 
    # واللغة العربية للقيم المعروضة في الأدمن (اليمين)
    STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
   ]
    
    # تأكدي من أن related_name هو 'signup_request' كما هو موجود لديكِ
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='signup_request')
    phone_number = models.CharField(max_length=15)
    
    # وثائق التحقق
    national_id = models.FileField(upload_to='helpers/ids/')
    moh_authorization = models.FileField(upload_to='helpers/auth/')
    training_certificates = models.FileField(upload_to='helpers/certs/', null=True, blank=True)
    
    # التأكد من أن max_length يكفي لكلمة 'APPROVED' و 'REJECTED'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # استخدام get_status_display() يعرض "مقبول" بدلاً من "APPROVED" في الأدمن
        return f"{self.user.get_full_name()} - {self.get_status_display()}"


# 3. الخدمات (التي سيختار منها أو يضيفها المساعد)
class Service(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True) # الكود الفريد الذي ناقشناه
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.specialty.name} - {self.name}"

# 4. بروفايل المساعد (المرحلة الثانية - بعد الاعتماد)
class HelperProfile(models.Model):
    # الربط مع المستخدم ليتوافق مع property (is_helper_approved)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='helper_profile' # تأكدي أن هذا الاسم يطابق المستخدم في كود زميلتك
    )
    
    bio = models.TextField(max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to='helpers/photos/', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(Service, blank=True)
    
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # حقل الحالة ليتوافق مع المنطق الجديد
    verification_status = models.CharField(
        max_length=10, 
        choices=SignupToHelpers.STATUS_CHOICES, 
        default='PENDING'
    )
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.verification_status})"

# 5. المواعيد والخبرات (مرتبطة بالبروفايل)
class Availability(models.Model):
    class Days(models.TextChoices):
        SUNDAY = 'SUN', 'Sunday'
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'

    helper = models.ForeignKey(HelperProfile, on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=3, choices=Days.choices)
    start_time = models.TimeField() 
    end_time = models.TimeField()   
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Availabilities"

class Experience(models.Model):
    helper = models.ForeignKey(HelperProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)
    description = models.TextField()
    years = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.title} - {self.helper.user.last_name}"