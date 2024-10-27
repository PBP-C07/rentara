import json
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from joinpartner.models import Partner, Vehicles

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('main/fixtures/dataset.json') as file:
            data = json.load(file)

            partners_created = {}
            # Pertama, buat partner
            for item in data:
                partner_id = item['fields']['toko']  # Menggunakan nama toko sebagai pengidentifikasi unik
                
                # Buat User jika belum ada
                user, created = User.objects.get_or_create(
                    username=partner_id,  # Gunakan nama toko sebagai username
                    defaults={
                        'first_name': partner_id,
                        'last_name': '',
                        'email': f"{partner_id}@example.com",  # Ganti dengan email yang valid jika ada
                        'password': 'defaultpassword'  # Set password default
                    }
                )

                # Buat Partner
                partner, created = Partner.objects.get_or_create(
                    user=user,
                    defaults={
                        'id': uuid.uuid4(),  # Hasilkan UUID untuk partner
                        'toko': partner_id,
                        'link_lokasi': item['fields']['link_lokasi'],
                        'notelp': str(item['fields']['notelp']),
                        'status': 'Approved'  # Atau status lain yang Anda inginkan
                    }
                )
                
                # Kemudian, buat kendaraan yang terkait dengan partner
                Vehicles.objects.create(
                    partner=partner,
                    link_foto=item['fields']['link_foto'],
                    merk=item['fields']['merk'],
                    tipe=item['fields']['tipe'],
                    jenis_kendaraan=item['fields']['jenis_kendaraan'],
                    warna=item['fields']['warna'],
                    harga=item['fields']['harga'],
                    bahan_bakar=item['fields'].get('bahan_bakar', ''),  # Default ke string kosong jika tidak ada
                    status=item['fields'].get('status', Vehicles.Sewa)  # Default ke 'Sewa' jika tidak disediakan
                )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
