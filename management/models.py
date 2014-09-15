from django.db import models

class Place(models.Model):

	#PLACE_CATEGORY_CHOICES = (('a','a'),('b','b'),('c','c'),)
    name = models.CharField(max_length=64)
    #category = models.CharField(max_length=32,choices=PLACE_CATEGORY_CHOICES)
    photo = models.CharField(max_length=512, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    open_hour = models.CharField(max_length=128, blank=True)
    latitude = models.FloatField(max_length=32, blank=True)
    longitude = models.FloatField(max_length=32, blank=True)
    news = models.TextField(max_length=512, blank=True)
    description = models.TextField(max_length=512, blank=True)

class Place_Category(models.Model):
    name = models.CharField(max_length=64)