from django.db import models
from accounts.models import User  # ✅ Correct import

REGION_CHOICES = [
    ('Riyadh', 'Riyadh'),
    ('Makkah', 'Makkah'),
    ('Madinah', 'Madinah'),
    ('Eastern', 'Eastern Province'),
    ('Qassim', 'Qassim'),
    ('Asir', 'Asir'),
    ('Tabuk', 'Tabuk'),
    ('Hail', 'Hail'),
    ('Northern', 'Northern Borders'),
    ('Jazan', 'Jazan'),
    ('Najran', 'Najran'),
    ('Bahah', 'Al Bahah'),
    ('Jawf', 'Al Jawf')
]

class School(models.Model):
    name = models.CharField(max_length=100)  # اسم المدرسة
    school_id = models.CharField(max_length=50)  # الرقم الوزاري أو الإحصائي
    location = models.CharField(max_length=255)  # الموقع (نص أو GPS)
    labs_count = models.IntegerField()  # عدد المعامل
    classes_count = models.IntegerField()  # عدد الفصول
    pc_needed = models.IntegerField()  # احتياج PC
    laptop_needed = models.IntegerField()  # احتياج Laptop
    projector_needed = models.IntegerField()  # احتياج Projector
    image = models.ImageField(upload_to='school_images/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    city = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='schools_added')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
