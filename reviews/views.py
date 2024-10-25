from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
    
