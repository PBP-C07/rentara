from django.test import TestCase, Client
from django.urls import reverse # check
from django.contrib.auth.models import User
from .models import Vehicle, Katalog
from joinpartner.models import Partner
from .forms import VehicleForm

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