from django.db import models
from main.models import Vehicle
from joinpartner.models import Partner

class Katalog(models.Model): # check
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    owner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.owner.toko} - {self.vehicle.merk} {self.vehicle.tipe}"