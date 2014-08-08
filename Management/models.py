from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=64)
    photo = models.CharField(max_length=512)
    latitude = models.FloatField(max_length=32)
    longitude = models.FloatField(max_length=32)
    phone = models.CharField(max_length=32)
    news = models.CharField(max_length=512)
    open_hours = models.CharField(max_length=128)

