from django.urls import path
from joinpartner.views import show_vehicle, join_partner, add_product, delete_product, edit_product, edit_profile, register, login_user, logout_user, manage_partners, approve_partner, reject_partner, pending_approval,rejected

app_name = 'joinpartner'

urlpatterns = [
    path('vehicles/', show_vehicle, name='show_vehicle'),
    path('vehicles/add/', add_product, name='add_product'),
    path('', join_partner, name='join_partner'),
    path('vehicles/<uuid:product_id>/edit/', edit_product, name='edit_product'),  # Ubah ke uuid
    path('vehicles/<uuid:product_id>/delete/', delete_product, name='delete_product'),  # Ubah ke uuid
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('manage_partners/', manage_partners, name='manage_partners'),
    path('approve_partner/<uuid:partner_id>/', approve_partner, name='approve_partner'),
    path('reject_partner/<uuid:partner_id>/', reject_partner, name='reject_partner'),
    path('pending-approval/', pending_approval, name='pending_approval'),
    path('rejected/', rejected, name='rejected'),
]