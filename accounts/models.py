from django.db import models
from django.contrib.auth.models import AbstractUser

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

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'أدمن'),
        ('technician', 'فني'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='technician')
    region = models.CharField(max_length=50, choices=REGION_CHOICES)  # قائمة منسدلة
    city = models.CharField(max_length=50)  # يدخلها المستخدم يدوي
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
