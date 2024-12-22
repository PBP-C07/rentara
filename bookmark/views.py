# views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from sewajual.models import Vehicle
from .models import Bookmark
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@login_required
def bookmark_list_flutter(request):
    bookmarked_vehicles = Bookmark.objects.filter(user=request.user).values_list('vehicle_id', flat=True)
    return JsonResponse({'bookmarked_vehicles': list(bookmarked_vehicles)})

@csrf_exempt
@login_required
def toggle_bookmark_flutter(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, vehicle=vehicle)
    
    if not created:
        bookmark.delete()
        is_bookmarked = False
    else:
        is_bookmarked = True
  
    # Handle Flutter (JSON response) and Web (redirect)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accepts('application/json'):
        return JsonResponse({'status': 'success', 'is_bookmarked': is_bookmarked})
    
    return redirect(request.META.get('HTTP_REFERER', reverse('vehicle_detail', args=[vehicle.id])))