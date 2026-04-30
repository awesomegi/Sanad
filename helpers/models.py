from django.db import models
from django.conf import settings
# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المدينة")

    class Meta:
        verbose_name = "مدينة"
        verbose_name_plural = "المدن"

    def __str__(self):
        return self.name