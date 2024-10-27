from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rentdriver.forms import DriverForm
from rentdriver.models import Driver
import json

def load_drivers_from_json(file_path = 'rentdriver/data/drivers.json'):
    with open(file_path) as file:
        drivers_data = json.load(file)
        for driver in drivers_data:
            # Check if the driver already exists by name (or any unique identifier)
            driver_instance, created = Driver.objects.get_or_create(
                name=driver['name'],
                defaults={
                    'phone_number': driver['phone_number'],
                    'vehicle_type': driver['vehicle_type'],
                    'experience_years': driver['experience_years'],
                }
            )

@login_required(login_url='main:login')
def show_main(request):
    load_drivers_from_json()

    drivers = Driver.objects.all()

    context = {
        'driver_entries': drivers,
    }

    return render(request, "rentdriver.html", context)

def add_driver_view(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rentdriver:show_main')  
    else:
        form = DriverForm()
    
    return render(request, 'add_driver.html', {'form': form})
