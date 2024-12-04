from django.db import models
from django.contrib.auth.models import User
import uuid

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make user optional
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('minibus', 'Minibus')
    ])

    EXPERIENCE_CHOICES = [
        ('2+', '2+ Years'),
        ('5+', '5+ Years'),
        ('7+', '7+ Years'),
        ('10+', '10+ Years')
    ]
    
    experience_years = models.CharField(
        max_length=3, 
        choices=EXPERIENCE_CHOICES, 
        default='2+'
    )
