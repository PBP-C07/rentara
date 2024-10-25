from django.db import models
from main.models import Vehicle

class Katalog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)