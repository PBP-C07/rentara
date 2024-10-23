from django.db import models
import uuid
from django.contrib.auth.models import User

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_name = models.CharField(max_length=255)
    gmaps_link = models.URLField(max_length=500)  # Langsung menyimpan link Google Maps
    phone_number = models.CharField(max_length=15)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    
    def get_whatsapp_link(self):
        # Menghasilkan link untuk menghubungi nomor telepon melalui WhatsApp
        return f"https://wa.me/{self.phone_number.replace('+', '')}"

    def __str__(self):
        return self.store_name
    
class Vehicle(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_image =  models.URLField(max_length=500)
    brand = models.CharField(max_length=100)
    brand_type = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)  # seperti mobil, motor, dll.
    color = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    AVAILABLE = 'tersedia'
    NOT_AVAILABLE = 'tidak tersedia'
    STATUS_CHOICES = [
        (AVAILABLE, 'Tersedia'),
        (NOT_AVAILABLE, 'Tidak Tersedia'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
    )