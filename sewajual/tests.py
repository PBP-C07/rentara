from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Vehicle, Katalog
from joinpartner.models import Partner, Vehicles
from .forms import VehicleForm
from django.contrib.messages import get_messages

class VehicleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='testpass')
        self.staff_user = User.objects.create_user(username='staff', password='staffpass', is_staff=True)
        self.partner = Partner.objects.create(
            user=self.user, toko='Test Shop', link_lokasi='https://maps.google.com/test', notelp='081234567890'
        )
        self.vehicle_data = {
            'toko': 'Test Shop', 'merk': 'Toyota', 'tipe': 'Avanza', 'warna': 'Hitam',
            'jenis_kendaraan': 'Mobil', 'harga': 150000000, 'status': 'Tersedia',
            'notelp': '081234567890', 'bahan_bakar': 'Bensin', 'link_lokasi': 'https://maps.google.com/test',
            'link_foto': 'https://example.com/photo.jpg'
        }

    def test_vehicle_list(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        response = self.client.get(reverse('sewajual:vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card_product.html')
        self.assertIn(vehicle, response.context['vehicles'])

    def test_full_info_authenticated(self):
        self.client.login(username='user', password='testpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        response = self.client.get(reverse('sewajual:full_info', args=[vehicle.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'full_info.html')

    def test_full_info_unauthenticated(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        response = self.client.get(reverse('sewajual:full_info', args=[vehicle.pk]))
        self.assertRedirects(response, f'/login/?next=/vehicle/{vehicle.pk}/full-info/')

    def test_admin_vehicle_list_staff(self):
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        response = self.client.get(reverse('sewajual:admin_vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card_admin.html')
        self.assertIn(vehicle, response.context['vehicles'])

    def test_add_vehicle_get(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('sewajual:add_vehicle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_vehicle.html')
        self.assertIsInstance(response.context['form'], VehicleForm)

    def test_add_vehicle_post_success(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.post(reverse('sewajual:add_vehicle'), self.vehicle_data)
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))
        self.assertTrue(Vehicle.objects.filter(merk='Toyota').exists())
        self.assertTrue(Katalog.objects.filter(vehicle__merk='Toyota').exists())

    def test_add_vehicle_post_ajax_success(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.post(
            reverse('sewajual:add_vehicle'), self.vehicle_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(Vehicle.objects.filter(merk='Toyota').exists())

    def test_add_vehicle_post_invalid_form(self):
        self.client.login(username='staff', password='staffpass')
        invalid_data = self.vehicle_data.copy()
        invalid_data['harga'] = 'invalid'
        response = self.client.post(reverse('sewajual:add_vehicle'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_vehicle.html')
        self.assertTrue(response.context['form'].errors)

    def test_add_vehicle_post_ajax_invalid_form(self):
        self.client.login(username='staff', password='staffpass')
        invalid_data = self.vehicle_data.copy()
        invalid_data['harga'] = 'invalid'
        response = self.client.post(
            reverse('sewajual:add_vehicle'), invalid_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_add_vehicle_post_invalid_partner(self):
        self.client.login(username='staff', password='staffpass')
        invalid_data = self.vehicle_data.copy()
        invalid_data['toko'] = 'Non-existent Shop'
        response = self.client.post(
            reverse('sewajual:add_vehicle'), invalid_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_edit_vehicle_get(self):
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        response = self.client.get(reverse('sewajual:edit_vehicle', args=[vehicle.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_vehicle.html')

    def test_edit_vehicle_post_success(self):
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        updated_data = self.vehicle_data.copy()
        updated_data['merk'] = 'Honda'
        response = self.client.post(reverse('sewajual:edit_vehicle', args=[vehicle.pk]), updated_data)
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.merk, 'Honda')

    def test_delete_vehicle_success(self):
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        Katalog.objects.create(vehicle=vehicle, owner=self.partner)
        response = self.client.post(reverse('sewajual:delete_vehicle', args=[vehicle.pk]))
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))
        self.assertFalse(Vehicle.objects.filter(pk=vehicle.pk).exists())
        self.assertFalse(Katalog.objects.filter(vehicle=vehicle).exists())

    def test_delete_vehicle_ajax_success(self):
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        Katalog.objects.create(vehicle=vehicle, owner=self.partner)
        response = self.client.post(
            reverse('sewajual:delete_vehicle', args=[vehicle.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertFalse(Vehicle.objects.filter(pk=vehicle.pk).exists())

    def test_delete_vehicle_ajax_error(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.post(
            reverse('sewajual:delete_vehicle', args=[999]), HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 404)
    
    def test_delete_vehicle_with_exception(self):
        """Test delete vehicle with exception handling"""
        self.client.login(username='staff', password='staffpass')
        
        # Buat vehicle dan katalog untuk dihapus
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        Katalog.objects.create(vehicle=vehicle, owner=self.partner)
        
        # Test non-AJAX request dengan invalid PK untuk trigger exception
        response = self.client.post(reverse('sewajual:delete_vehicle', args=[99999]))
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Error" in str(m) for m in messages))

    def test_delete_vehicle_ajax_with_exception(self):
        """Test delete vehicle with AJAX exception handling"""
        self.client.login(username='staff', password='staffpass')
        
        # Test AJAX request dengan invalid PK untuk trigger exception
        response = self.client.post(
            reverse('sewajual:delete_vehicle', args=[99999]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_full_info_vehicles_model(self):
        """Test full info view when vehicle found in Vehicles model"""
        self.client.login(username='user', password='testpass')
        
        # Create vehicle in Vehicles model
        vehicle_data = {
            'toko': 'Test Shop',
            'merk': 'Honda',
            'tipe': 'Jazz'
        }
        vehicles_obj = Vehicles.objects.create(**vehicle_data)
        
        response = self.client.get(reverse('sewajual:full_info', args=[vehicles_obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'full_info.html')
        self.assertEqual(response.context['vehicle'], vehicles_obj)

    def test_edit_vehicle_post_invalid_form(self):
        """Test edit vehicle with invalid form data"""
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        
        invalid_data = self.vehicle_data.copy()
        invalid_data['harga'] = 'invalid_price'
        
        response = self.client.post(
            reverse('sewajual:edit_vehicle', args=[vehicle.pk]),
            invalid_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_vehicle.html')
        self.assertTrue(response.context['form'].errors)
        
        # Verify vehicle data remains unchanged
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.harga, self.vehicle_data['harga'])

    def test_delete_vehicle_error_messages(self):
        """Test error messages in delete vehicle view"""
        self.client.login(username='staff', password='staffpass')
        
        # Create vehicle and catalog
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        Katalog.objects.create(vehicle=vehicle, owner=self.partner)
        
        # Test with non-AJAX request
        response = self.client.post(reverse('sewajual:delete_vehicle', args=[vehicle.pk]))
        messages = list(get_messages(response.wsgi_request))
        
        # Verify success message
        self.assertEqual(len(messages), 1)
        self.assertTrue('berhasil dihapus' in str(messages[0]))
        
        # Verify redirect
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))

    def test_add_vehicle_error_messages(self):
        """Test specific error messages in add vehicle"""
        self.client.login(username='staff', password='staffpass')
        
        # Test invalid form tanpa AJAX
        invalid_data = self.vehicle_data.copy()
        invalid_data['harga'] = 'invalid'
        response = self.client.post(reverse('sewajual:add_vehicle'), invalid_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Form tidak valid" in str(m) for m in messages))

    def test_edit_vehicle_post_invalid(self):
        """Test edit vehicle dengan form tidak valid"""
        self.client.login(username='staff', password='staffpass')
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        
        # Test invalid form
        invalid_data = self.vehicle_data.copy()
        invalid_data['harga'] = 'bukan angka'
        response = self.client.post(
            reverse('sewajual:edit_vehicle', args=[vehicle.pk]),
            invalid_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_vehicle.html')
        self.assertFalse(response.context['form'].is_valid())
        
        # Verify data tidak berubah
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.harga, self.vehicle_data['harga'])

    def test_delete_vehicle_non_ajax_error(self):
        """Test delete vehicle non-ajax dengan error"""
        self.client.login(username='staff', password='staffpass')
        
        # Test dengan invalid pk
        response = self.client.post(reverse('sewajual:delete_vehicle', args=[99999]))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Error" in str(m) for m in messages))
        self.assertRedirects(response, reverse('sewajual:admin_vehicle_list'))

    def test_delete_vehicle_ajax_not_found(self):
        """Test delete vehicle ajax dengan vehicle tidak ditemukan"""
        self.client.login(username='staff', password='staffpass')
        
        # Test AJAX request dengan invalid pk
        response = self.client.post(
            reverse('sewajual:delete_vehicle', args=[99999]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 404)