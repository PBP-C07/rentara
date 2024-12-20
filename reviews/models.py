from django.db import models
from django.contrib.auth.models import User
from sewajual.models import Vehicle
import uuid

class Reviews(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.vehicle}"