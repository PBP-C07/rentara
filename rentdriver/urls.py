from django.urls import path
from rentdriver.views import show_drivers

app_name = 'rentdriver'

urlpatterns = [
    path('', show_drivers, name='show_drivers'),
]