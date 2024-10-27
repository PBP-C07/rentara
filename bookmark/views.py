# views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
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

    if not created:
        bookmark.delete()  # Remove bookmark if it already exists
    
    next_page = request.GET.get('next', 'sewajual:vehicle_list')
    if next_page == 'bookmark':
        return redirect('bookmark:bookmarked_vehicles')
    
    return redirect('sewajual:full_info', pk=vehicle_id)