from django.urls import path,include
from joinpartner.views import show_vehicle, join_partner, add_product, delete_product, edit_product, manage_partners, approve_partner, reject_partner, pending_approval,rejected, list_partner, delete_partner, show_partner_json, show_vehicle_partner, check_partner_status, create_vehicle_flutter, get_partner, edit_vehicle_flutter, get_detail_vehicle, delete_vehicle_flutter

app_name = 'joinpartner'

urlpatterns = [path('vehicles/show/', show_vehicle, name='show_vehicle'),
    path('vehicles/add/', add_product, name='add_product'),
    path('join_partner', join_partner, name='join_partner'),
    path('vehicles/<uuid:product_id>/edit/', edit_product, name='edit_product'),
    path('vehicles/<uuid:product_id>/delete/', delete_product, name='delete_product'),
    path('manage_partners/', manage_partners, name='manage_partners'),
    path('approve_partner/<uuid:partner_id>/', approve_partner, name='approve_partner'),
    path('reject_partner/<uuid:partner_id>/', reject_partner, name='reject_partner'),
    path('pending-approval/', pending_approval, name='pending_approval'),
    path('rejected/', rejected, name='rejected'),
    path('list_partner/', list_partner, name='list_partner'),
    path('delete_partner/<uuid:partner_id>/', delete_partner, name='delete_partner'),
    path('json_by_partner/',show_vehicle_partner, name='show_json_byPartner'),
    path('partner_json/', show_partner_json, name='show_partner_json'),
    path('check_status/', check_partner_status, name='check_status'),
    path('create_vehicle_flutter/', create_vehicle_flutter, name='create_vehicle_flutter'),
    path('get_partner/', get_partner, name='get_partner'),
    path('edit_vehicle_flutter/<str:vehicle_id>/', edit_vehicle_flutter, name='edit_vehicle_flutter'),
    path('vehicle_detail_flutter/<str:vehicle_id>/', get_detail_vehicle, name='vehicle_detail_flutter'),
    path('delete_vehicle_flutter/<str:vehicle_id>/', delete_vehicle_flutter, name='delete_vehicle_flutter'),
    ]
