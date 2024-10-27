from django import forms
from django.forms import ModelForm
from main.models import Vehicle
from joinpartner.models import Partner

class VehicleForm(ModelForm):
    store_name = forms.ModelChoiceField(
        queryset=Partner.objects.all(),
        to_field_name="store_name",
        label="Pilih Toko",
        required=True,
    )

    class Meta:
        model = Vehicle
        fields = ['merk', 'tipe', 'jenis_kendaraan', 'warna', 'harga', 'status', 'notelp', 'bahan_bakar', 'link_lokasi', 'link_foto']