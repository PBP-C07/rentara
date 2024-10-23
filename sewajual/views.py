from django.shortcuts import render, get_object_or_404
from .models import Vehicle

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'card_product.html', {'vehicles': vehicles})

def full_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'full_info.html', {'vehicle': vehicle})