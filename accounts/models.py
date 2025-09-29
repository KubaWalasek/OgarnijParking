from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    door_number = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username