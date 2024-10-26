import uuid
from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} ({self.brand})"

class Report(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('mismatch', 'Kendaraan tidak sesuai merek yang dipesan'),
        ('damaged', 'Kendaraan rusak'),
        ('service', 'Pelayanan tidak ramah'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reports')
    issue_type = models.CharField(max_length=10, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')

    def __str__(self):
        return f"{self.issue_type()} - {self.vehicle.type}"
