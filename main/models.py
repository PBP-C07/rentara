from django.db import models
import uuid

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    toko = models.CharField(max_length=255)
    merk = models.CharField(max_length=100)
    tipe = models.CharField(max_length=100)
    warna = models.CharField(max_length=100)
    jenis_kendaraan = models.CharField(max_length=50)
    harga = models.IntegerField()
    status = models.CharField(max_length=50)
    notelp = models.CharField(max_length=15, null=True)
    bahan_bakar = models.CharField(max_length=50)
    link_lokasi = models.URLField()
    link_foto = models.URLField()