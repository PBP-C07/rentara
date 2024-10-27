from django.urls import path
from bookmark.views import show_main, add_bookmark, remove_bookmark

app_name = 'bookmark'

urlpatterns = [
    path('bookmarked/', show_main, name='show_main'),
    path('add-bookmark/<uuid:vehicle_id>/', add_bookmark, name='add_bookmark'),
    path('remove-bookmark/<uuid:vehicle_id>/', remove_bookmark, name='remove_bookmark'),
]