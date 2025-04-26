from django.db import models
from schools.models import School  # ✅ correct import
from accounts.models import User   # ✅ added this line

class Device(models.Model):
    DEVICE_TYPES = [
        ('PC', 'PC'),
        ('Laptop', 'Laptop'),
        ('Projector', 'Projector'),
        ('Switch', 'Switch'),
        ('Router', 'Router'),
        ('Access Point', 'Access Point'),
        ('Screen', 'Interactive Screen'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Excellent', 'ممتاز'),
        ('Good', 'جيد'),
        ('Poor', 'ضعيف'),
    ]

    OS_CHOICES = [
        ('Windows 7', 'Windows 7'),
        ('Windows 10', 'Windows 10'),
        ('Windows 11', 'Windows 11'),
        ('Android', 'Android'),
        ('NA', 'N/A'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="devices")
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPES)
    serial_number = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    operating_system = models.CharField(max_length=30, choices=OS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_type} - {self.serial_number}"
