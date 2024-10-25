from django import forms
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "merk", "tipe", "jenis_kendaraan", "status",
            "warna", "bahan_bakar", "harga", "foto", "link_lokasi"
        ]

    JENIS_CHOICES = [
        ('', 'Pilih Jenis'),
        ('mobil', 'Mobil'),
        ('motor', 'Motor'),
    ]

    STATUS_CHOICES = [
        ('', 'Pilih Status'),
        ('tersedia', 'Tersedia'),
        ('tidak_tersedia', 'Tidak Tersedia'),
    ]

    BAHAN_BAKAR_CHOICES = [
        ('', 'Pilih Bahan Bakar'),
        ('bensin', 'Bensin'),
        ('solar', 'Solar'),
        ('listrik', 'Listrik'),
    ]

    # Field definitions with proper validation
    merk = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Merk kendaraan harus diisi'}
    )
    
    tipe = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Tipe kendaraan harus diisi'}
    )
    
    jenis_kendaraan = forms.ChoiceField(
        choices=JENIS_CHOICES,
        required=True,
        error_messages={'required': 'Jenis kendaraan harus dipilih'}
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=True,
        error_messages={'required': 'Status kendaraan harus dipilih'}
    )
    
    warna = forms.CharField(
        max_length=50,
        required=False
    )
    
    bahan_bakar = forms.ChoiceField(
        choices=BAHAN_BAKAR_CHOICES,
        required=False
    )
    
    harga = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        error_messages={
            'required': 'Harga harus diisi',
            'invalid': 'Harga tidak valid'
        }
    )
    
    foto = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp']
            )
        ],
        error_messages={
            'invalid_extension': 'Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau WEBP.',
            'invalid_image': 'File yang diunggah bukan gambar yang valid.'
        }
    )
    
    link_lokasi = forms.URLField(
        required=False,
        error_messages={'invalid': 'URL lokasi tidak valid'}
    )

    def clean_merk(self):
        merk = self.cleaned_data.get('merk')
        if merk:
            merk = merk.strip()
            if len(merk) < 2:
                raise ValidationError('Merk terlalu pendek')
        return merk

    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga and harga <= 0:
            raise ValidationError('Harga harus lebih besar dari 0')
        return harga

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Ukuran file terlalu besar. Maksimal 5MB.')
        return foto