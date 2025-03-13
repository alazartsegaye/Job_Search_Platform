from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
