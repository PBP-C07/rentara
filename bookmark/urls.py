from django.urls import path
from . import views

app_name = 'bookmark'  # This sets the namespace to 'bookmark'

urlpatterns = [
    path('toggle/<uuid:vehicle_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('list/', views.bookmarked_vehicles, name='bookmarked_vehicles'),
    path('bookmark/list/', views.bookmark_list_flutter, name='bookmark_list'),
    path('bookmark/toggle/<uuid:vehicle_id>/', views.toggle_bookmark_flutter, name='toggle_bookmark_flutter'),
]
