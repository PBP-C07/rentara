import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from reviews.forms import ReviewsForm
from reviews.models import Reviews
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from django.utils.html import strip_tags
from sewajual.models import Vehicle
from django.db.models import Avg

def show_reviews(request):
    review_entries = Reviews.objects.all()

    context = {
        'review_entries': review_entries
    }

    return render(request, "show_review.html", context)

@login_required(login_url='/login')
def create_reviews(request):
    form = ReviewsForm(request.POST or None)
    vehicles = Vehicle.objects.all()

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        return redirect('reviews:show_reviews')
    
    context = {'form': form, 'vehicles': vehicles}
    return render(request, "create_review.html", context)
    
def edit_review(request, id):
    review = Reviews.objects.get(pk = id)
    vehicles = Vehicle.objects.all()
    form = ReviewsForm(request.POST or None, instance=review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reviews:show_reviews'))
    context = {'form': form, 'vehicles': vehicles}
    return render(request, "edit_review.html", context)

def delete_review(request, id):
    review = Reviews.objects.get(pk = id)
    review.delete()
    return HttpResponseRedirect(reverse('reviews:show_reviews'))

def review_list(request):
    reviews = Reviews.objects.all()
    formatted_reviews = []
    
    for review in reviews:
        formatted_review = {
            'title': review.title,
            'vehicle': review.vehicle,
            'user': review.user,
            'time': review.time.strftime("%d/%m/%y"),
            'rating': review.rating,
            'description': review.description,
        }
        formatted_reviews.append(formatted_review)

    return render(request, 'card_review.html', {'reviews': formatted_reviews})

def show_xml(request, vehicle_id=None):
    if vehicle_id:
        data = Reviews.objects.filter(vehicle_id=vehicle_id)
    else:
        data = Reviews.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request, vehicle_id=None):
    if vehicle_id:
        data = Reviews.objects.filter(vehicle_id=vehicle_id)
    else:
        data = Reviews.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Reviews.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Reviews.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def create_reviews_ajax(request):
    title = strip_tags(request.POST.get("title"))
    title = request.POST.get("title")
    rating = request.POST.get("rating")
    description = strip_tags(request.POST.get("description"))
    user = request.user

    vehicles = Vehicle.objects.all()
    vehicles_data = [{"merk": v.merk, "tipe": v.tipe, "warna": v.warna} for v in vehicles]

    new_review = Reviews(
        title=title, rating=rating,
        description=description,
        user=user
    )
    new_review.save()

    return JsonResponse({
        "status": "CREATED",
        "vehicles": vehicles_data
    }, status=201)

@csrf_exempt
def create_reviews_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        vehicle_id = uuid.UUID(data["vehicle"])
        vehicle = Vehicle.objects.get(pk=vehicle_id)

        new_product = Reviews.objects.create(
            user=request.user,
                title=data["title"],
                vehicle=vehicle, 
                rating=int(data["rating"]),
                description=data["description"]        
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_reviews_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle_id = uuid.UUID(data["vehicle"])
            vehicle = Vehicle.objects.get(pk=vehicle_id)

            review = Reviews.objects.get(user=request.user, vehicle=vehicle)

            review.title = data.get("title", review.title)
            review.vehicle = vehicle
            review.rating = int(data.get("rating", review.rating))
            review.description = data.get("description", review.description)
            
            review.save()

            return JsonResponse({"status": "success", "message": "Review updated successfully"}, status=200)
        except Reviews.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found or not authorized to edit this review"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
def delete_reviews_flutter(request):
    if request.method == 'GET':
        try:
            review_id = request.GET.get("id")
            
            if not review_id:
                return JsonResponse({"status": "error", "message": "Review ID is required"}, status=400)

            review = Reviews.objects.get(pk=review_id, user=request.user)
            review.delete()

            return JsonResponse({"status": "success", "message": "Review deleted successfully"}, status=200)
        except Reviews.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found or not authorized to delete this review"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
def get_vehicle_review_stats(request, vehicle_id):
    try:
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        reviews = Reviews.objects.filter(vehicle=vehicle)
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return JsonResponse({
            'average_rating': round(average_rating, 1),
            'review_count': total_reviews,
        })
    except ValueError:
        return JsonResponse({'error': 'Invalid vehicle ID'}, status=400)


@csrf_exempt
def get_current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'user_id': request.user.id,
            'username': request.user.username,
            'is_authenticated': True
        })
    return JsonResponse({
        'user_id': None,
        'username': None,
        'is_authenticated': False
    })

@csrf_exempt
def show_reviews_json(request):
    reviews = Reviews.objects.all()
    return JsonResponse(
        [
            {
                "model": "reviews.reviews",
                "pk": str(review.pk),
                "fields": {
                    "title": review.title,
                    "user": review.user.id,  
                    "vehicle": str(review.vehicle.pk) if review.vehicle else None, 
                    "time": review.time.isoformat(),
                    "rating": review.rating,
                    "description": review.description,
                }
            }
            for review in reviews
        ],
        safe=False
    )