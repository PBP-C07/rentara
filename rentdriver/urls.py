from django.urls import path
from rentdriver.views import show_main, add_driver_view

app_name = 'rentdriver'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-driver-view', add_driver_view, name='add_driver_view'), 
]