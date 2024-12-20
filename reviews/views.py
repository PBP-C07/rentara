from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from reviews.forms import ReviewsForm
from reviews.models import Reviews
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from django.utils.html import strip_tags
from django.db.models import Avg

from sewajual.models import Vehicle

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

def show_xml(request):
    data = Reviews.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Reviews.objects.filter(user=request.user)
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

    new_review = Reviews(
        title=title, rating=rating,
        description=description,
        user=user
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)

def review_kendaraan(request, pk):
    kendaraan = Vehicle.objects.get(pk=pk)
    reviews = Reviews.objects.filter(kendaraan=kendaraan)

    # Hitung rata-rata rating, default ke 0.0 jika tidak ada ulasan
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0

    context = {
        'kendaraan': kendaraan,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'kendaraan_detail.html', context)

def reviews_by_vehicle(request):
    review_entries = Reviews.objects.select_related('vehicle').all()

    grouped_reviews = defaultdict(list)
    for review in review_entries:
        vehicle_key = f"{review.vehicle.merk} {review.vehicle.tipe}"
        grouped_reviews[vehicle_key].append(review)

    vehicle_ratings = {
        vehicle_key: {
            "average_rating": Reviews.objects.filter(vehicle=review.vehicle).aggregate(Avg('rating'))['rating__avg'] or 0.0,
            "reviews": reviews
        }
        for vehicle_key, reviews in grouped_reviews.items()
    }

    context = {
        'vehicle_ratings': vehicle_ratings
    }

    return render(request, "reviews_by_vehicle.html", context)