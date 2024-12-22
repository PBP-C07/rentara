from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Vehicle
from joinpartner.models import Partner
from bookmark.models import Bookmark
from .forms import VehicleForm
from django.db.models import Avg

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
    vehicles = list(Vehicle.objects.all())

    for vehicle in vehicles:
        vehicle.harga = format_price(vehicle.harga)
        reviews = vehicle.reviews.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        vehicle.average_rating = average_rating
    
    return render(request, 'card_product.html', {'vehicles': vehicles})

@login_required(login_url='main:login')
def full_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    html_file = 'full_info.html'

    vehicle.harga = format_price(vehicle.harga)
    
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, vehicle=vehicle).exists()

    reviews = vehicle.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()

    next_page = request.GET.get('next', 'vehicle_list')

    return render(request, html_file, {
        'vehicle': vehicle,
        'is_bookmarked': is_bookmarked,
        'average_rating': average_rating,
        'review_count': review_count,
        'next_page': next_page
    })

@staff_member_required
@login_required(login_url='main:login')
def admin_vehicle_list(request):
    vehicles = list(Vehicle.objects.all())
    form = VehicleForm()
    return render(request, 'card_admin.html', {'vehicles': vehicles, 'form': form})

@staff_member_required
@csrf_exempt
@require_POST
def add_vehicle(request):
    try:
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.toko = form.cleaned_data['toko']
            # Get partner based on toko and set it
            partner = get_object_or_404(Partner, toko=vehicle.toko)
            vehicle.partner = partner
            vehicle.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Kendaraan berhasil ditambahkan',
                'id': str(vehicle.pk),
                'merk': vehicle.merk,
                'tipe': vehicle.tipe
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Form tidak valid!',
                'errors': form.errors
            }, status=400)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

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
def delete_vehicle(request, pk):
    if request.method == 'POST':
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.delete()
            return JsonResponse({'status': 'success',
                'message': 'Kendaraan berhasil dihapus'})
                
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def show_json(request):
    data = list(Vehicle.objects.all())
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@login_required
def get_stores(request):
    stores = Partner.objects.filter(status='Approved')
    store_list = [{"toko": store.toko} for store in stores]  
    return JsonResponse(store_list, safe=False)

import json # tessss
@csrf_exempt
@require_http_methods(["POST"]) 
def create_product_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_vehicle = Vehicle.objects.create(
            toko=data["toko"],
            merk=data["merk"],
            tipe=data["tipe"],
            warna=data["warna"],
            jenis_kendaraan=data["jenis_kendaraan"],
            harga=int(data["harga"]),
            status=data["status"],
            notelp=data.get("notelp"),
            bahan_bakar=data["bahan_bakar"],
            link_lokasi=data["link_lokasi"],
            link_foto=data["link_foto"],
            partner=Partner.objects.get(id=data["partner_id"]) if "partner_id" in data else None
        )

        new_vehicle.save()


        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_vehicle_flutter(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle = get_object_or_404(Vehicle, pk=pk)
            
            vehicle.toko = data["toko"]
            vehicle.merk = data["merk"]
            vehicle.tipe = data["tipe"]
            vehicle.warna = data["warna"]
            vehicle.jenis_kendaraan = data["jenis_kendaraan"]
            vehicle.harga = int(data["harga"])
            vehicle.status = data["status"]
            vehicle.notelp = data["notelp"]
            vehicle.bahan_bakar = data["bahan_bakar"]
            vehicle.link_lokasi = data["link_lokasi"]
            vehicle.link_foto = data["link_foto"]
            
            vehicle.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Vehicle updated successfully!"
            })
        except Vehicle.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Vehicle not found"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)