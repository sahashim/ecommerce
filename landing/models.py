# Create your models here.
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()