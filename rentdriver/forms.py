from django.forms import ModelForm
from rentdriver.models import Driver

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ["name", "phone_number", "vehicle_type", "experience_years"]