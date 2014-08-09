from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=64)
    photo = models.CharField(max_length=512)
    phone = models.CharField(max_length=32)
    category = models.CharField(max_length=512)
    open_hour = models.CharField(max_length=128)
    latitude = models.FloatField(max_length=32)
    longitude = models.FloatField(max_length=32)
    news = models.TextField(max_length=512)
    description = models.TextField(max_length=512)


