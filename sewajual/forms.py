from django import forms
from django.forms import ModelForm
from sewajual.models import Vehicle
from joinpartner.models import Partner

class VehicleForm(ModelForm):
    toko = forms.ModelChoiceField(
        queryset=Partner.objects.filter(status='Approved'),
        to_field_name="toko",
        label="Pilih Toko",
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-teal focus:ring-1 focus:ring-teal transition-colors duration-200',
            'id': 'id_toko'
        })
    )

    class Meta:
        model = Vehicle
        fields = ['toko', 'merk', 'tipe', 'jenis_kendaraan', 'warna', 'harga', 'status', 'notelp', 'bahan_bakar', 'link_lokasi', 'link_foto']