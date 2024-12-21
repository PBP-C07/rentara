import uuid
from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.BooleanField(default=True)

class Report(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('Mismatch', 'Kendaraan tidak sesuai yang dipesan'),
        ('Damaged', 'Kendaraan rusak'),
        ('Service', 'Pelayanan tidak ramah'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.CharField(max_length=255)
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Tambahkan field status
