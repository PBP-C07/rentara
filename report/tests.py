from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Vehicle, Report
from datetime import datetime
from django.utils import timezone
from django.core import serializers
import uuid
import json

class ReportTests(TestCase):
    def setUp(self):
        # Set up a test client, test user, and test data for vehicles and reports
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.vehicle1 = Vehicle.objects.create(type='Sedan', brand='Toyota', rental_price=100.00, availability=True)
        self.vehicle2 = Vehicle.objects.create(type='SUV', brand='Honda', rental_price=200.00, availability=True)
        self.report_data = {
            "vehicle": self.vehicle1.type,
            "issue_type": "Mismatch",
            "description": "The vehicle did not match the order",
        }
        self.client.login(username='testuser', password='password')

    def test_create_report_entry_get(self):
        # Test GET request for create_report_entry view
        response = self.client.get(reverse('report:create_report_entry'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_report.html')
        self.assertIn('form', response.context)
        self.assertIn('vehicles', response.context)

    def test_create_report_entry_post(self):
        # Test successful POST request for create_report_entry view
        response = self.client.post(reverse('report:create_report_entry'), self.report_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:show_main'))
        self.assertEqual(Report.objects.count(), 1)

    def test_add_report_get(self):
        # Test GET request for add_report view
        response = self.client.get(reverse('report:add_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_form.html')

    def test_add_report_post(self):
        # Test POST request for add_report view
        response = self.client.post(reverse('report:add_report'), self.report_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report:create_report_entry'))
        self.assertEqual(Report.objects.count(), 1)

    def test_edit_report_get(self):
        # Test GET request for edit_report view
        report = Report.objects.create(user=self.user, **self.report_data)
        response = self.client.get(reverse('report:edit_report', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_report.html')

    def test_edit_report_post(self):
        # Test successful POST request for edit_report view
        report = Report.objects.create(user=self.user, **self.report_data)
        updated_data = {"vehicle": "Updated Vehicle", "issue_type": "Damaged", "description": "Updated description"}
        response = self.client.post(reverse('report:edit_report', args=[report.id]), updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report:create_report_entry'))
        report.refresh_from_db()
        self.assertEqual(report.vehicle, "Updated Vehicle")
        self.assertEqual(report.issue_type, "Damaged")

    def test_delete_report(self):
        # Test delete_report view
        report = Report.objects.create(user=self.user, **self.report_data)
        response = self.client.post(reverse('report:delete_report', args=[report.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('report:create_report_entry'))
        self.assertEqual(Report.objects.count(), 0)

    def test_show_xml(self):
        # Test show_xml view
        Report.objects.create(user=self.user, **self.report_data)
        response = self.client.get(reverse('report:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        # Test show_json view
        Report.objects.create(user=self.user, **self.report_data)
        response = self.client.get(reverse('report:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        # Test show_xml_by_id view
        report = Report.objects.create(user=self.user, **self.report_data)
        response = self.client.get(reverse('report:show_xml_by_id', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        # Test show_json_by_id view
        report = Report.objects.create(user=self.user, **self.report_data)
        response = self.client.get(reverse('report:show_json_by_id', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_report_entry_ajax_post(self):
        # Test report_entry_ajax view
        data = {
            "vehicle": "Sedan",
            "description": "An issue with the vehicle",
            "issue_type": "Service"
        }
        response = self.client.post(reverse('report:report_entry_ajax'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"CREATED")
        self.assertEqual(Report.objects.count(), 1)

    def test_vehicle_model(self):
        # Test Vehicle model creation
        vehicle = Vehicle.objects.create(type='Truck', brand='Ford', rental_price=300.00, availability=False)
        self.assertEqual(vehicle.type, 'Truck')
        self.assertEqual(vehicle.brand, 'Ford')
        self.assertFalse(vehicle.availability)

    def test_report_model(self):
        # Test Report model creation
        report = Report.objects.create(user=self.user, vehicle='Truck', issue_type='Mismatch', description='Test description')
        self.assertEqual(report.vehicle, 'Truck')
        self.assertEqual(report.issue_type, 'Mismatch')
        self.assertEqual(report.description, 'Test description')

    def test_access_create_report_entry_without_login(self):
        # Test that a user cannot access create_report_entry view without login
        self.client.logout()
        response = self.client.get(reverse('report:create_report_entry'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
    def test_invalid_form_submission(self):
        response = self.client.post(reverse('report:add_report'), {})
        self.assertEqual(response.status_code, 200)  # Stay on the form page
        self.assertIn('form', response.context)  # Check form is in context
        form = response.context['form']
        self.assertFormError(response, 'form', 'vehicle', 'This field is required.')

    # Add more tests as needed for edge cases and additional functionality
