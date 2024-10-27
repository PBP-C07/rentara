from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Driver
from .forms import DriverForm
import json

User = get_user_model()

class DriverViewTests(TestCase):

    def setUp(self):
        # Create a user for login
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a staff user for edit tests
        self.staff_user = User.objects.create_user(username='staffuser', password='testpass', is_staff=True)

        # Create a driver instance for testing
        self.driver = Driver.objects.create(
            name='John Doe',
            phone_number='123-456-7890',
            vehicle_type='Sedan',
            experience_years=5,
        )

    def test_show_main_view(self):
        """Test the main driver view returns a 200 status code and renders the correct template."""
        response = self.client.get(reverse('show_main'))  # Replace with your actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentdriver.html')  # Check that the correct template is used
        self.assertContains(response, 'John Doe')  # Verify that the driver's name appears in the response

    def test_edit_driver_view_get(self):
        """Test the edit driver view GET request returns the correct form and renders the template."""
        self.client.login(username='staffuser', password='testpass')  # Log in as staff
        response = self.client.get(reverse('edit_driver', args=[self.driver.id]))  # Replace with your actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_driver.html')  # Check the correct template is used
        self.assertContains(response, 'John Doe')  # Verify the driver's name appears in the form

    def test_edit_driver_view_post(self):
        """Test the edit driver view POST request successfully updates driver data."""
        self.client.login(username='staffuser', password='testpass')  # Log in as staff
        form_data = {
            'name': 'Jane Doe',
            'phone_number': '987-654-3210',
            'vehicle_type': 'SUV',
            'experience_years': 6,
        }
        response = self.client.post(reverse('edit_driver', args=[self.driver.id]), data=form_data)  # Replace with your actual URL name
        self.assertEqual(response.status_code, 302)  # Check for a redirect after successful update
        self.driver.refresh_from_db()  # Refresh the driver instance from the database
        self.assertEqual(self.driver.name, 'Jane Doe')  # Verify the driver's name is updated
        self.assertEqual(self.driver.phone_number, '987-654-3210')  # Verify the phone number is updated

    def test_edit_driver_view_post_ajax(self):
        """Test the edit driver view handles AJAX POST requests correctly."""
        self.client.login(username='staffuser', password='testpass')  # Log in as staff
        form_data = {
            'name': 'Jane Doe',
            'phone_number': '987-654-3210',
            'vehicle_type': 'SUV',
            'experience_years': 6,
        }
        response = self.client.post(reverse('edit_driver', args=[self.driver.id]), data=form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # Simulate an AJAX request
        self.assertEqual(response.status_code, 200)  # Check for success response
        json_response = json.loads(response.content)
        self.assertTrue(json_response['success'])  # Ensure the JSON response indicates success

    def test_load_drivers_from_json(self):
        """Test loading drivers from JSON file."""
        # Create a JSON file with test data
        json_data = [
            {
                "name": "Alice Smith",
                "phone_number": "555-1234",
                "vehicle_type": "Van",
                "experience_years": 3
            },
            {
                "name": "Bob Brown",
                "phone_number": "555-5678",
                "vehicle_type": "Truck",
                "experience_years": 4
            }
        ]
        with open('rentdriver/data/drivers.json', 'w') as file:
            json.dump(json_data, file)

        # Call the function to load drivers
        from rentdriver.views import load_drivers_from_json  # Import the function to test
        load_drivers_from_json('rentdriver/data/drivers.json')  # Load drivers from the created JSON

        # Check that the drivers are created in the database
        self.assertTrue(Driver.objects.filter(name='Alice Smith').exists())
        self.assertTrue(Driver.objects.filter(name='Bob Brown').exists())
