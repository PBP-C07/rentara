from django.urls import path
from reviews.views import show_reviews, create_reviews, edit_review, delete_review

app_name = 'reviews'

urlpatterns = [
    path('show-reviews/', show_reviews, name='show_reviews'),
    path('create-reviews/', create_reviews, name='create_reviews'),
    path('edit-review/<uuid:id>', edit_review, name='edit_review'),
    path('delete/<uuid:id>', delete_review, name='delete_review'),
]