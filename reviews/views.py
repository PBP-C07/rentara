from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from reviews.forms import ReviewsForm
from reviews.models import Reviews

def show_reviews(request):
    review_entries = Reviews.objects.all()

    context = {
        'review_entries': review_entries
    }

    return render(request, "show_review.html", context)

@login_required(login_url='/login')
def create_reviews(request):
    form = ReviewsForm(request.POST or None)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        return redirect('reviews:show_reviews')
    
    context = {'form': form}
    return render(request, "create_review.html", context)
    
def edit_review(request, id):
    review = get_object_or_404(Reviews, pk=id)
    form = ReviewsForm(request.POST or None, instance=review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reviews:show_reviews'))
    context = {'form': form}
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
            'user': review.user,
            'time': review.time.strftime("%d/%m/%y"),
            'rating': review.rating,
            'description': review.description,
        }
        formatted_reviews.append(formatted_review)

    return render(request, 'card_review.html', {'reviews': formatted_reviews})