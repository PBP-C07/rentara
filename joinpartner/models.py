from django.db import models
import uuid
from django.contrib.auth.models import User

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
    
    def get_whatsapp_link(self):
        # Menghasilkan link untuk menghubungi nomor telepon melalui WhatsApp
        return f"https://wa.me/{self.notelp.replace('+', '')}"

    def __str__(self):
        return self.toko
    
class Vehicles(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='vehicles')
    link_foto =  models.URLField(max_length=500)
    merk = models.CharField(max_length=100)
    tipe = models.CharField(max_length=100)
    jenis_kendaraan = models.CharField(max_length=100)  # seperti mobil, motor, dll.
    warna = models.CharField(max_length=50)
    harga = models.IntegerField()
    Sewa = 'Sewa'
    Jual = 'Jual'
    STATUS_CHOICES = [
        (Sewa, 'Sewa'),
        (Jual, 'Jual'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=Sewa
    )