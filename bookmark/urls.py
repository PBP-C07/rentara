from django.urls import path
from . import views

app_name = 'bookmark'  # This sets the namespace to 'bookmark'

urlpatterns = [
    path('toggle/<uuid:vehicle_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('list/', views.bookmarked_vehicles, name='bookmarked_vehicles'),
]
