from django.urls import path
from report.views import create_report_entry, show_reports, show_json, show_xml, show_json_by_id, show_xml_by_id, login_user  

app_name = 'report'


urlpatterns = [
    path('', show_reports, name='report_list'),
    path('login/', login_user, name='login'),
    path('create_report_entry', create_report_entry, name='create_report_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'), 
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]
