from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Partner, Vehicles
from joinpartner.forms import VehicleForm, PartnerForm
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
        
    def test_edit_product(self):
        # Create an initial vehicle to edit
        vehicle = Vehicles.objects.create(
            partner=self.partner,
            link_foto='http://example.com/image.jpg',
            merk='Old Merk',
            tipe='Old Tipe',
            jenis_kendaraan='Sedan',
            warna='Blue',
            harga='50000',
            status='Sewa',
            bahan_bakar='Diesel'
        )
        # URL for editing the vehicle
        url = reverse('joinpartner:edit_product', args=[vehicle.id])
        # New data to update the vehicle
        data = {
            'link_foto': 'http://example.com/image_new.jpg',
            'merk': 'New Merk',
            'tipe': 'New Tipe',
            'jenis_kendaraan': 'Hatchback',
            'warna': 'Green',
            'harga': '60000',
            'status': 'Jual',
            'bahan_bakar': 'Petrol'
        }
        # Perform the POST request to edit the vehicle
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Check for successful response
        vehicle.refresh_from_db()  # Refresh the vehicle instance from the database
        self.assertEqual(vehicle.merk, 'New Merk')  # Check if the vehicle's merk has been updated
        self.assertEqual(vehicle.tipe, 'New Tipe')  # Check if the vehicle's tipe has been updated

    def test_join_partner(self):
        # Attempt to join as a partner
        url = reverse('joinpartner:join_partner')
        data = {
            'toko': 'New Test Store',
            'link_lokasi': 'http://example.com/new',
            'notelp': '987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Check for successful response
        self.assertTrue(Partner.objects.filter(toko='New Test Store').exists())  # Ensure partner is created

        # Attempt to join again as the same partner
        response = self.client.post(url, data)  # Attempt to create the same partner again
        self.assertEqual(response.status_code, 200)  # Check for successful response
        self.assertEqual(Partner.objects.filter(user=self.user).count(), 1)  # Ensure still only one partner exists


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
        self.assertEqual(response.status_code, 400)
        self.assertIn('merk', response.json()['errors'])
        self.assertIn('tipe', response.json()['errors'])

    def test_list_vehicle_search(self):
        response = self.client.get(reverse('joinpartner:show_vehicle'), {'query': 'Toyota'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')
    
    def test_join_partner(self):
        url = reverse('joinpartner:join_partner')
        data = {
            'toko': 'New Test Store',
            'link_lokasi': 'http://example.com/new',
            'notelp': '987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Partner.objects.filter(toko='New Test Store').exists())

    def test_delete_partner(self):
        url = reverse('joinpartner:delete_partner', args=[self.partner.id])
        response = self.client.post(url)  # Make sure to use POST for delete action
        self.assertEqual(response.status_code, 200)  # Check for redirect
        self.assertFalse(Partner.objects.filter(id=self.partner.id).exists())  # Ensure partner is deleted
    
    def test_vehicle_form_valid(self):
        data = {
            'link_foto': 'http://example.com/image.jpg',
            'merk': '<b>Brand</b>',
            'tipe': '<i>Type</i>',
            'jenis_kendaraan': '<script>alert("Car")</script>',
            'warna': 'Red',
            'harga': 50000,
            'status': 'Sewa',
            'bahan_bakar': 'Petrol'
        }
        form = VehicleForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['merk'], 'Brand')
        self.assertEqual(form.cleaned_data['tipe'], 'Type')
        self.assertEqual(form.cleaned_data['jenis_kendaraan'], 'alert("Car")')
        self.assertEqual(form.cleaned_data['warna'], 'Red')
        self.assertEqual(form.cleaned_data['bahan_bakar'], 'Petrol')

    def test_vehicle_form_invalid(self):
        data = {
            'link_foto': '',
            'merk': '',
            'tipe': '',
            'jenis_kendaraan': '',
            'warna': '',
            'harga': '',
            'status': '',
            'bahan_bakar': ''
        }
        form = VehicleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('merk', form.errors)
        self.assertIn('tipe', form.errors)
        self.assertIn('jenis_kendaraan', form.errors)
        self.assertIn('warna', form.errors)
        self.assertIn('harga', form.errors)
        self.assertIn('status', form.errors)
        self.assertIn('bahan_bakar', form.errors)
    