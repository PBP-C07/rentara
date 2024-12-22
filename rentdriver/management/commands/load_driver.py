from django.core.management.base import BaseCommand
from rentdriver.models import Driver
import uuid

class Command(BaseCommand):
    help = 'Loads driver data into the database'

    def handle(self, *args, **kwargs):
        drivers_data = [
           {"name": "Andi Pratama", "phone_number": "+62-812-3456", "vehicle_type": "Van", "experience_years": "3+"},
            {"name": "Budi Santoso", "phone_number": "+62-813-4567", "vehicle_type": "Truck", "experience_years": "5+"},
            {"name": "Citra Dewi", "phone_number": "+62-814-5678", "vehicle_type": "Motorcycle", "experience_years": "2+"},
            {"name": "Dwi Putra", "phone_number": "+62-815-6789", "vehicle_type": "Car", "experience_years": "4+"},
            {"name": "Eka Permana", "phone_number": "+62-816-7890", "vehicle_type": "Van", "experience_years": "6+"},
            {"name": "Fahmi Ardiansyah", "phone_number": "+62-817-8901", "vehicle_type": "Truck", "experience_years": "7+"},
            {"name": "Gina Sari", "phone_number": "+62-818-9012", "vehicle_type": "Motorcycle", "experience_years": "1+"},
            {"name": "Hadi Susanto", "phone_number": "+62-819-0123", "vehicle_type": "Car", "experience_years": "8+"},
            {"name": "Indah Lestari", "phone_number": "+62-820-1234", "vehicle_type": "Van", "experience_years": "3+"},
            {"name": "Joko Santoso", "phone_number": "+62-821-2345", "vehicle_type": "Truck", "experience_years": "5+"},
            {"name": "Kiki Rahmawati", "phone_number": "+62-822-3456", "vehicle_type": "Motorcycle", "experience_years": "4+"},
            {"name": "Lia Suryani", "phone_number": "+62-823-4567", "vehicle_type": "Car", "experience_years": "2+"},
            {"name": "Miko Prasetyo", "phone_number": "+62-824-5678", "vehicle_type": "Van", "experience_years": "6+"},
            {"name": "Nina Widya", "phone_number": "+62-825-6789", "vehicle_type": "Truck", "experience_years": "7+"},
            {"name": "Oka Jaya", "phone_number": "+62-826-7890", "vehicle_type": "Motorcycle", "experience_years": "1+"},
            {"name": "Penny Yuliana", "phone_number": "+62-827-8901", "vehicle_type": "Car", "experience_years": "9+"},
            {"name": "Rudi Haryanto", "phone_number": "+62-828-9012", "vehicle_type": "Van", "experience_years": "4+"},
            {"name": "Santi Dewi", "phone_number": "+62-829-0123", "vehicle_type": "Truck", "experience_years": "5+"},
            {"name": "Taufik Hidayat", "phone_number": "+62-830-1234", "vehicle_type": "Motorcycle", "experience_years": "3+"},
            {"name": "Uli Siti", "phone_number": "+62-831-2345", "vehicle_type": "Car", "experience_years": "6+"}
        ]

        for driver_data in drivers_data:
            driver, created = Driver.objects.get_or_create(
                id=uuid.uuid4(),
                name=driver_data["name"],
                phone_number=driver_data["phone_number"],
                vehicle_type=driver_data["vehicle_type"].lower(),
                experience_years=driver_data["experience_years"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Driver {driver.name} created."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Driver {driver.name} already exists."))
