from django.urls import path
from reviews.views import show_reviews, create_reviews, edit_review, delete_review, create_reviews_ajax
from reviews.views import show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'reviews'

urlpatterns = [
    path('show-reviews/', show_reviews, name='show_reviews'),
    path('create-reviews/', create_reviews, name='create_reviews'),
    path('edit-review/<uuid:id>/', edit_review, name='edit_review'),
    path('delete/<uuid:id>/', delete_review, name='delete_review'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('create-reviews-ajax', create_reviews_ajax, name='create_reviews_ajax'),
]