from django.urls import path
from report.views import create_report_entry, show_reports, show_json, show_xml, show_json_by_id, show_xml_by_id, login_user  , report_entry_ajax, edit_report, delete_report, add_report

app_name = 'report'

app_name = 'report'

urlpatterns = [
    path('show_reports', show_reports, name='report_list'),
    path('create_report_entry', create_report_entry, name='create_report_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'), 
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('report-entry-ajax', report_entry_ajax, name='report_entry_ajax'),
    path('edit-report/<uuid:id>', edit_report, name='edit_report'),
    path('delete/<uuid:id>', delete_report, name='delete_report'), 
    path('add_report', add_report, name='add_report'), 


]
