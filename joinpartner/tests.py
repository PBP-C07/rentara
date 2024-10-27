from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Partner, Vehicles
import uuid

class VehicleManagementTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a test partner linked to the user
        self.partner = Partner.objects.create(
            user=self.user,
            toko="Test Toko",
            link_lokasi="https://maps.google.com/test",
            notelp="081234567890",
            status='Approved'
        )
        
        # Create a test vehicle linked to the partner
        self.vehicle = Vehicles.objects.create(
            partner=self.partner,
            link_foto="https://example.com/image.jpg",
            merk="Toyota",
            tipe="Avanza",
            jenis_kendaraan="Mobil",
            warna="Merah",
            harga=500000,
            status="Sewa"
        )
        
        self.client.login(username='testuser', password='password')

    def test_show_vehicle_view(self):
        response = self.client.get(reverse('joinpartner:show_vehicle'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Avanza")
    
    def test_add_vehicle(self):
        response = self.client.post(reverse('joinpartner:add_product'), {
            'link_foto': 'https://example.com/image2.jpg',
            'merk': 'Honda',
            'tipe': 'Civic',
            'jenis_kendaraan': 'Mobil',
            'warna': 'Hitam',
            'harga': '600000',
            'status': 'Sewa'
        })
        self.assertEqual(response.status_code, 200)  # Redirect after successful addition
        self.assertEqual(Vehicles.objects.filter(merk='Honda').count(), 1)
        
    def test_edit_vehicle(self):
        response = self.client.post(reverse('joinpartner:edit_product', args=[self.vehicle.id]), {
            'link_foto': 'https://example.com/image3.jpg',
            'merk': 'Toyota',
            'tipe': 'Fortuner',
            'jenis_kendaraan': 'Mobil',
            'warna': 'Hitam',
            'harga': '750000',
            'status': 'Sewa',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        updated_vehicle = Vehicles.objects.get(id=self.vehicle.id)
        self.assertEqual(updated_vehicle.tipe, 'Fortuner')
        self.assertEqual(updated_vehicle.warna, 'Hitam')

    def test_delete_vehicle(self):
        response = self.client.post(reverse('joinpartner:delete_product', args=[self.vehicle.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertEqual(Vehicles.objects.filter(id=self.vehicle.id).count(), 0)
    
    def test_approve_partner(self):
        # Set the partner status to Pending
        self.partner.status = 'Pending'
        self.partner.save()
        
        self.client.force_login(User.objects.create_superuser(username='admin', password='admin', email='admin@example.com'))
        response = self.client.post(reverse('joinpartner:approve_partner', args=[self.partner.id]))
        self.assertEqual(response.status_code, 200)
        self.partner.refresh_from_db()
        self.assertEqual(self.partner.status, 'Approved')

    def test_reject_partner(self):
        # Set the partner status to Pending
        self.partner.status = 'Pending'
        self.partner.save()
        
        self.client.force_login(User.objects.create_superuser(username='admin', password='admin', email='admin@example.com'))
        response = self.client.post(reverse('joinpartner:reject_partner', args=[self.partner.id]))
        self.assertEqual(response.status_code, 200)
        self.partner.refresh_from_db()
        self.assertEqual(self.partner.status, 'Rejected')

    def test_list_approved_partners(self):
        self.partner.status = 'Approved'
        self.partner.save()
        
        response = self.client.get(reverse('joinpartner:list_partner'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Toko")

    def test_add_vehicle_with_empty_fields(self):
        response = self.client.post(reverse('joinpartner:add_product'), {
            'link_foto': '',
            'merk': '',
            'tipe': '',
            'jenis_kendaraan': '',
            'warna': '',
            'harga': '',
            'status': '',
            'bahan_bakar': ''
        })
        self.assertEqual(response.status_code, 400)  # Expecting a 400 error for validation
        self.assertIn('merk', response.json()['errors'])
        self.assertIn('tipe', response.json()['errors'])
        self.assertIn('harga', response.json()['errors'])
        self.assertIn('bahan_bakar', response.json()['errors'])

    def test_edit_vehicle_with_empty_fields(self):
        response = self.client.post(reverse('joinpartner:edit_product', args=[self.vehicle.id]), {
            'link_foto': '',
            'merk': '',
            'tipe': '',
            'jenis_kendaraan': '',
            'warna': '',
            'harga': '',
            'status': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('merk', response.json()['errors'])
        self.assertIn('tipe', response.json()['errors'])

    def test_list_vehicle_search(self):
        response = self.client.get(reverse('joinpartner:show_vehicle'), {'query': 'Toyota'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')