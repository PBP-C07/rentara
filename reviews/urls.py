from django.urls import path
from reviews.views import show_reviews, create_reviews 

app_name = 'reviews'

urlpatterns = [
    path('show-reviews/', show_reviews, name='show_reviews'),
    path('create-reviews/', create_reviews, name='create_reviews'),
]