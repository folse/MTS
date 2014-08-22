from django.db import models
from django.contrib.auth.models import User

class User_Profile(models.Model):
    user = models.OneToOneField(User)
    objectId = models.CharField(max_length=256)
    userType = models.IntegerField(default=1)
    description = models.TextField(max_length=256)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = User_Profile.objects.get_or_create(user=instance)