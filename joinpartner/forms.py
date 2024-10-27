from django import forms
from django.forms import ModelForm
from joinpartner.models import Vehicles, Partner
from django.utils.html import strip_tags

class VehicleForm(ModelForm):
    class Meta :
        model = Vehicles
        fields = ['link_foto', 'merk', 'tipe', 'jenis_kendaraan', 'warna', 'harga', 'status']
    def clean_merk(self):
        merk = self.cleaned_data["merk"]
        return strip_tags(merk)

    def clean_tipe(self):
        tipe = self.cleaned_data["tipe"]
        return strip_tags(tipe)

    def clean_jenis_kendaraan(self):
        jenis_kendaraan = self.cleaned_data["jenis_kendaraan"]
        return strip_tags(jenis_kendaraan)

    def clean_color(self):
        color = self.cleaned_data["color"]
        return strip_tags(color)

    

class PartnerForm(ModelForm):
    class Meta : 
        model = Partner
        fields = ['toko', 'link_lokasi', 'notelp']
    def clean_store(self):
        toko = self.cleaned_data["toko"]
        return strip_tags(toko)

    def clean_gmaps(self):
        link_lokasi = self.cleaned_data["link_lokasi"]
        return strip_tags(link_lokasi)

    def clean_number(self):
        notelp= self.cleaned_data["notelp"]
        return strip_tags(notelp)

