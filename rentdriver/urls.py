from django.urls import path
from rentdriver.views import show_main, edit_driver, manage_drivers, get_drivers, edit_driver_flutter

app_name = 'rentdriver'

urlpatterns = [
    path('manage_drivers/', manage_drivers, name='manage_drivers'),
    path('edit_driver/<uuid:driver_id>/', edit_driver, name='edit_driver'),
    path('show-main/', show_main, name='show_main'),
    path('driver/json/', get_drivers, name='get_drivers'),
    path('driver/edit/<uuid:driver_id>/', edit_driver_flutter, name='edit_driver_flutter'),

]