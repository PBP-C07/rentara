from django.urls import path
from .views import vehicle_list, full_info

urlpatterns = [
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicle/<int:pk>/', full_info, name='full_info'),
]