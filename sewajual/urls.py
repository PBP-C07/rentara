from django.urls import path
from .views import vehicle_list, full_info, AdminVehicleDeleteView, AdminVehicleUpdateView, AdminVehicleListView, AdminVehicleCreateView

urlpatterns = [
    path('katalog/', vehicle_list, name='vehicle_list'),
    path('katalog/<uuid:pk>/', full_info, name='full_info'),
    path('admin/vehicles/', AdminVehicleListView.as_view(), name='admin-vehicles'),
    path('admin/vehicles/add/', AdminVehicleCreateView.as_view(), name='admin-vehicle-add'),
    path('admin/vehicles/<uuid:pk>/edit/', AdminVehicleUpdateView.as_view(), name='admin-vehicle-edit'),
    path('admin/vehicles/<uuid:pk>/delete/', AdminVehicleDeleteView.as_view(), name='admin-vehicle-delete'),
]