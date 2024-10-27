# views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sewajual.models import Vehicle
from .models import Bookmark

@login_required
def bookmarked_vehicles(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('vehicle')
    return render(request, 'bookmark.html', {'bookmarks': bookmarks})

@login_required
def toggle_bookmark(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, vehicle=vehicle)
    if created:
        messages.success(request, "Vehicle bookmarked successfully!")
    else:
        bookmark.delete()  # Unbookmark if it already exists
        messages.info(request, "Bookmark removed.")
    return redirect('sewajual:full_info', pk=vehicle_id)