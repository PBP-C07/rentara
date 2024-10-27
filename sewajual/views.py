from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.contrib import messages
from .models import Vehicle, Katalog
from joinpartner.models import Vehicles, Partner
from bookmark.models import Bookmark
from .forms import VehicleForm

def format_price(value):
    try:
        formatted = str(int(float(value)))
        result = ""
        while len(formatted) > 3:
            result = "." + formatted[-3:] + result
            formatted = formatted[:-3]
        return formatted + result
    except (ValueError, TypeError):
        return value

def vehicle_list(request):
    vehicles = list(Vehicle.objects.all()) + list(Vehicles.objects.all())
    for vehicle in vehicles:
        vehicle.harga = format_price(vehicle.harga)
    
    return render(request, 'card_product.html', {'vehicles': vehicles})

@login_required(login_url='main:login')
def full_info(request, pk):
    try:
        # Attempt to fetch from the `Vehicle` model first
        vehicle = get_object_or_404(Vehicle, pk=pk)
        html_file = 'full_info.html'
    except:
        # If not found, retrieve from `Vehicles` and transform to `Vehicle` format
        vehicles = get_object_or_404(Vehicles, pk=pk)
        vehicle = Vehicle(
            id=vehicles.id,
            toko=vehicles.partner.toko, 
            merk=vehicles.merk,
            tipe=vehicles.tipe,
            jenis_kendaraan=vehicles.jenis_kendaraan,
            warna=vehicles.warna,
            harga=vehicles.harga,
            status=vehicles.status,
            bahan_bakar=vehicles.bahan_bakar,
            link_foto=vehicles.link_foto,
            link_lokasi=vehicles.partner.link_lokasi,
            notelp=vehicles.partner.notelp
        )
        html_file = 'full_info.html'

    vehicle.harga = format_price(vehicle.harga)
    
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, vehicle=vehicle).exists()

    next_page = request.GET.get('next', 'vehicle_list')

    return render(request, html_file, {
        'vehicle': vehicle,
        'is_bookmarked': is_bookmarked,
        'next_page': next_page
    })

@staff_member_required
def admin_vehicle_list(request):
    vehicles = list(Vehicle.objects.all()) + list(Vehicles.objects.all())
    return render(request, 'card_admin.html', {'vehicles': vehicles})

@staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_vehicle(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            try:
                vehicle = form.save(commit=False)
                vehicle.toko = form.cleaned_data['toko']
                vehicle.save()
                
                Katalog.objects.create(
                    vehicle=vehicle, 
                    owner=get_object_or_404(Partner, toko=vehicle.toko)
                )
                
                if is_ajax:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Kendaraan berhasil ditambahkan',
                        'id': vehicle.pk,
                        'merk': vehicle.merk,
                        'tipe': vehicle.tipe
                    })
                
                return redirect('sewajual:admin_vehicle_list')
                
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400) if is_ajax else messages.error(request, str(e))
        
        if is_ajax:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        messages.error(request, "Form tidak valid.")
            
    return render(request, 'add_vehicle.html', {'form': VehicleForm()})

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

    return render(request, 'edit_vehicle.html', {'form': form, 'vehicle': vehicle})

@staff_member_required
@csrf_exempt
@require_POST
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    try:
        Katalog.objects.filter(vehicle=vehicle).delete()
        vehicle.delete()
        
        if is_ajax:
            return JsonResponse({
                'status': 'success',
                'message': 'Data kendaraan berhasil dihapus'
            })
        
        messages.success(request, 'Data kendaraan berhasil dihapus')
        return redirect('sewajual:admin_vehicle_list')
    except Exception as e:
        if is_ajax:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        
        messages.error(request, f"Error: {str(e)}")
        return redirect('sewajual:admin_vehicle_list')