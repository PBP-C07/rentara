from django.urls import path
from rentdriver.views import show_main, edit_driver, manage_drivers

app_name = 'rentdriver'

urlpatterns = [
    path('manage_drivers/', manage_drivers, name='manage_drivers'),
    path('edit_driver/<uuid:driver_id>/', edit_driver, name='edit_driver'),
    path('show-main/', show_main, name='show_main'),
]