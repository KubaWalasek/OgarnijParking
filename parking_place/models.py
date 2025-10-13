from django.utils import timezone
from django.conf import settings
from django.db import models

class DistrictName(models.Model):
    district_name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if self.district_name:
            self.district_name = self.district_name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.district_name

class District(models.Model):
    district_name = models.ForeignKey(DistrictName, on_delete=models.PROTECT)
    signed_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='signed_user')

    def __str__(self):
        return str(self.district_name)

class ParkingPlaceData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    place_number = models.CharField(default=1)
    available_from = models.DateTimeField(default=timezone.now)
    available_until = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.district.district_name} - {self.place_number}'








