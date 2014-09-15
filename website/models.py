#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# class PlaceModel(models.Model):
#     user = models.OneToOneField(User)
#     objectId = models.CharField(max_length=256)
#     name = models.CharField(max_length=32)
#     address = models.CharField(max_length=256)
#     category = models.CharField(max_length=128)
#     phone = models.CharField(max_length=32)
#     #photo = models.CharField(max_length=512)
#     open_hour = models.CharField(max_length=128)
#     latitude = models.CharField(max_length=32)
#     longitude = models.CharField(max_length=32)
#     news = models.CharField(max_length=512)
#     description = models.CharField(max_length=512)