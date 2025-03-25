from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=16, null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    @property
    def is_employer(self):
        return self.jobs.exists()

    @property
    def is_applicant(self):
        return self.jobapplication_set.exists()

    def __str__(self):
        return self.username