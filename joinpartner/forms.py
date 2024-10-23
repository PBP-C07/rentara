from django import forms
from django.forms import ModelForm
from joinpartner.models import Vehicle, Partner
from django.utils.html import strip_tags

class VehicleForm(ModelForm):
    class Meta :
        model = Vehicle
        fields = ['vehicle_image', 'brand', 'brand_type', 'vehicle_type', 'color', 'price_per_day', 'status']
    def clean_brand(self):
        brand = self.cleaned_data["brand"]
        return strip_tags(brand)

    def clean_brand_type(self):
        brand_type = self.cleaned_data["brand_type"]
        return strip_tags(brand_type)

    def clean_vehicle_type(self):
        vehicle_type = self.cleaned_data["vehicle_type"]
        return strip_tags(vehicle_type)

    def clean_color(self):
        color = self.cleaned_data["color"]
        return strip_tags(color)

    

class PartnerForm(ModelForm):
    class Meta : 
        model = Partner
        fields = ['store_name', 'gmaps_link', 'phone_number']
    def clean_store(self):
        store_name = self.cleaned_data["store_name"]
        return strip_tags(store_name)

    def clean_gmaps(self):
        gmaps_link = self.cleaned_data["gmaps_link"]
        return strip_tags(gmaps_link)

    def clean_number(self):
        phone_number= self.cleaned_data["phone_number"]
        return strip_tags(phone_number)

class vehicleFilter(forms.Form):
    brand_type_filter = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Jenis Brand misal : vario'}))
    brand_filter = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Merek kendaraan misal : honda'}))
