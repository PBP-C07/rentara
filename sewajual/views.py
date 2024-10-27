from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Vehicle, Katalog
from joinpartner.models import Vehicles, Partner # check
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from .forms import VehicleForm
from django.contrib import messages
from django.http import JsonResponse

def vehicle_list(request):
    vehicles = list(Vehicle.objects.all()) + list(Vehicles.objects.all())
    return render(request, 'card_product.html', {'vehicles': vehicles})

@login_required(login_url='main:login')
def full_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicles = get_object_or_404(Vehicles, pk=pk)
    return render(request, 'full_info.html', {'vehicle': vehicle, 'vehicles': vehicles})

@staff_member_required
def admin_vehicle_list(request):
   vehicles = list(Vehicle.objects.all()) + list(Vehicles.objects.all())
   return render(request, 'card_admin.html', {'vehicles': vehicles})

@staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            try:
                vehicle = form.save(commit=False)
                toko = form.cleaned_data['toko']
                partner = get_object_or_404(Partner, toko=toko)
                vehicle.toko = toko
                vehicle.save()

                Katalog.objects.create(vehicle=vehicle, owner=partner)

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Kendaraan berhasil ditambahkan',
                        'id': vehicle.pk,
                        'merk': vehicle.merk,
                        'tipe': vehicle.tipe
                    })

                messages.success(request, "Kendaraan berhasil ditambahkan.")
                return redirect('sewajual:admin_vehicle_list')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
                messages.error(request, f"Error: {str(e)}")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Form tidak valid',
                    'errors': form.errors
                }, status=400)
            messages.error(request, "Form tidak valid.")
    else:
        form = VehicleForm()

    return render(request, 'add_vehicle.html', {'form': form})

@staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('sewajual:admin_vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'edit_vehicle.html', {'form': form})

@staff_member_required
@csrf_exempt
@require_POST
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    try:
        Katalog.objects.filter(vehicle=vehicle).delete()
        vehicle.delete()
        response = {'status': 'success', 'message': 'Data kendaraan berhasil dihapus'}
        if is_ajax:
            return JsonResponse(response)
        
        messages.success(request, response['message'])
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        if is_ajax:
            return JsonResponse(response, status=400)
        messages.error(request, f"Error: {response['message']}")
    
    return redirect('sewajual:admin_vehicle_list')