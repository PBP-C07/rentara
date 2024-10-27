from django.db import models
from django.contrib.auth.models import User
import uuid

class Reviews(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField()
    description = models.TextField()
    helpful_votes = models.PositiveIntegerField(default=0)