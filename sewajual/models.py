from django.db import models
from main.models import Vehicle
from django.contrib.auth.models import User

class Katalog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_vehicles', blank=True)
