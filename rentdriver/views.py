from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rentdriver.forms import DriverForm
from rentdriver.models import Driver
from django.http import JsonResponse
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

from django.http import JsonResponse


@staff_member_required
@login_required(login_url='main:login')
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                # Send a JSON response if the request is AJAX
                return JsonResponse({
                    'success': True,
                    'name': driver.name,
                    'phone_number': driver.phone_number,
                    'vehicle_type': driver.vehicle_type,
                    'experience_years': driver.experience_years,
                })
            return redirect('show_main')
    else:
        form = DriverForm(instance=driver)

    if request.is_ajax():
        # Render the form as HTML for an AJAX GET request
        return render(request, 'partials/edit_driver_form.html', {'form': form, 'driver': driver})
    return render(request, 'edit_driver.html', {'form': form, 'driver': driver})
