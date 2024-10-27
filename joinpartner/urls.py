from django.urls import path,include
from joinpartner.views import show_vehicle, join_partner, add_product, delete_product, edit_product, edit_profile, manage_partners, approve_partner, reject_partner, pending_approval,rejected, list_partner, delete_partner

app_name = 'joinpartner'

urlpatterns = [path('vehicles/', show_vehicle, name='show_vehicle'),
    path('vehicles/add/', add_product, name='add_product'),
    path('', join_partner, name='join_partner'),
    path('vehicles/<uuid:product_id>/edit/', edit_product, name='edit_product'),
    path('vehicles/<uuid:product_id>/delete/', delete_product, name='delete_product'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('manage_partners/', manage_partners, name='manage_partners'),
    path('approve_partner/<uuid:partner_id>/', approve_partner, name='approve_partner'),
    path('reject_partner/<uuid:partner_id>/', reject_partner, name='reject_partner'),
    path('pending-approval/', pending_approval, name='pending_approval'),
    path('rejected/', rejected, name='rejected'),
    # path('list_partner/', list_partner, name='list_partner'),
    # path('delete_partner/<uuid:partner_id>/', delete_partner, name='delete_partner'),
    ]