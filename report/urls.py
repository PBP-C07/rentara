from django.urls import path
from report.views import create_report_entry

urlpatterns = [
    path('create_report_entry', create_report_entry, name='create_report_entry'),
]
