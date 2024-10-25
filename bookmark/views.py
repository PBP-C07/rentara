from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sewajual.models import Vehicle
from .models import Bookmark

@login_required
def show_main(request):
    # Fetch all bookmarked vehicles for the logged-in user
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('vehicle')
    
    # Pass the bookmarked vehicles to the template
    return render(request, 'bookmarks/bookmarked_vehicles.html', {'bookmarks': bookmarks})

@login_required
def add_bookmark(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, vehicle=vehicle)
    
    if created:
        messages.success(request, "Vehicle bookmarked successfully!")
    else:
        messages.info(request, "This vehicle is already bookmarked.")

    return redirect('vehicle_detail', vehicle_id=vehicle.id)

@login_required
def remove_bookmark(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    Bookmark.objects.filter(user=request.user, vehicle=vehicle).delete()
    messages.success(request, "Bookmark removed successfully.")
    
    return redirect('vehicle_detail', vehicle_id=vehicle.id)

