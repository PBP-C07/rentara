from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Vehicle
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from .forms import VehicleForm
from bookmark.models import Bookmark

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'card_product.html', {'vehicles': vehicles})

@staff_member_required
def admin_vehicle_list(request):
   vehicles = Vehicle.objects.all()
   return render(request, 'card_admin.html', {'vehicles': vehicles})

# @staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sewajual:admin_vehicle_list')
    else:
        form = VehicleForm()

    return render(request, 'vehicle_form.html', {'form': form})

# @staff_member_required
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

    return render(request, 'vehicle_form.html', {'form': form, 'vehicle': vehicle})

# @staff_member_required
@csrf_exempt
@require_POST
def delete_vehicle(request, pk):
    try:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return HttpResponse(b"DELETED", status=200)
    except:
        return HttpResponse(b"ERROR", status=500)

@login_required(login_url='main:login')
def full_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, vehicle=vehicle).exists()

    next_page = request.GET.get('next', 'vehicle_list')  # Default to vehicle list if 'next' is not provided

    return render(request, 'full_info.html', {
        'vehicle': vehicle,
        'is_bookmarked': is_bookmarked,
        'next_page': next_page
    })