from http.client import HTTPResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rentdriver.forms import DriverForm
from rentdriver.models import Driver
from django.http import JsonResponse
from django.core import serializers

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

    return render(request, "rentdriver.html", {'driver_entries': drivers, 'user': request.user})

from django.shortcuts import render
import json

@staff_member_required
def manage_drivers(request):
    load_drivers_from_json()
    drivers = Driver.objects.all()
    
    # Convert QuerySet to a list of dictionaries, converting UUID to string
    drivers_list = [
        {
            'id': str(driver.id),  # Convert UUID to string
            'name': driver.name,
            'phone_number': driver.phone_number,
            'vehicle_type': driver.vehicle_type,
            'experience_years': driver.experience_years
        }
        for driver in drivers
    ] 
    return render(request, 'manage_driver.html', {'driver_entries': json.dumps(drivers_list), 'user': request.user})

@staff_member_required
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)  # Fetch the driver by UUID

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('rentdriver:manage_drivers')  # Redirect back to driver list after saving
    else:
        form = DriverForm(instance=driver)  # Pre-fill form with driver data

    return render(request, 'edit_driver_form.html', {'form': form, 'driver': driver})

@csrf_exempt
@login_required(login_url='main:login')
def edit_driver_flutter(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'phone_number', 'vehicle_type', 'experience_years']
            if not all(field in data for field in required_fields):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required fields'
                }, status=400)
            
            # Update driver fields
            driver.name = data['name']
            driver.phone_number = data['phone_number']
            driver.vehicle_type = data['vehicle_type']
            driver.experience_years = data['experience_years']
            
            driver.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Driver updated successfully'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
def get_drivers(request):
    drivers = Driver.objects.all()
    driver_list = [
        {
            'id': str(driver.id),
            'name': driver.name,
            'phone_number': driver.phone_number,
            'vehicle_type': driver.vehicle_type,
            'experience_years': driver.experience_years
        }
        for driver in drivers
    ]
    return JsonResponse(driver_list, safe=False)


