from django.db import models
import uuid
from django.contrib.auth.models import User
from main.models import Vehicle

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    toko = models.CharField(max_length=255)
    link_lokasi = models.URLField(max_length=500)  # Langsung menyimpan link Google Maps
    notelp = models.CharField(max_length=15)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    # vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    
    def get_whatsapp_link(self):
        # Menghasilkan link untuk menghubungi nomor telepon melalui WhatsApp
        return f"https://wa.me/{self.notelp.replace('+', '')}"

    def __str__(self):
        return self.toko
    

    
# class PartnerVehicle(models.Model):
#     partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)