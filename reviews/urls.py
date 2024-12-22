from django.urls import path
from authentication import views
from reviews.views import create_reviews_flutter, delete_reviews_flutter, edit_reviews_flutter, get_vehicle_review_stats, show_reviews, create_reviews, edit_review, delete_review, create_reviews_ajax
from reviews.views import show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'reviews'

urlpatterns = [
    path('show-reviews/', show_reviews, name='show_reviews'),
    path('create-reviews/', create_reviews, name='create_reviews'),
    path('edit-review/<uuid:id>/', edit_review, name='edit_review'),
    path('delete/<uuid:id>/', delete_review, name='delete_review'),
    path('show-reviews/xml/', show_xml, name='show_xml'),
    path('show-reviews/xml/<uuid:vehicle_id>/', show_json, name='show_json_by_vehicle'),
    path('show-reviews/json/', show_json, name='show_json'),
    path('show-reviews/json/<uuid:vehicle_id>/', show_json, name='show_json_by_vehicle'),
    path('show-reviews/xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('show-reviews/json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('create-reviews-ajax/', create_reviews_ajax, name='create_reviews_ajax'),
    path('create-reviews-flutter/', create_reviews_flutter, name='create_reviews_flutter'),
    path('edit-reviews-flutter/', edit_reviews_flutter, name='edit_reviews_flutter'),
    path('delete-reviews-flutter/', delete_reviews_flutter, name='delete_reviews_flutter'),
    path('vehicle_review_stats/<int:vehicle_id>/', get_vehicle_review_stats, name='vehicle_review_stats'),
]