from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import re


class DistrictName(models.Model):
    district_name = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('district_name'),
                name='uniq_district_name_ci'
            )
        ]
    def save(self, *args, **kwargs):
        if self.district_name:
            self.district_name = self.district_name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.district_name

class PostCode(models.Model):
    post_code = models.CharField(max_length=6)
    def clean(self):
        super().clean()
        if not re.match(r'^\d{2}-\d{3}$', self.post_code or ''):
            raise ValidationError({'post_code': 'Kod pocztowy musi być w formacie 00-000.'})

    def __str__(self):
        return self.post_code

class StreetName(models.Model):
    street_name = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('street_name'),
                name='uniq_street_name_ci'
            )
        ]
    def save(self, *args, **kwargs):
        if self.street_name:
            self.street_name = self.street_name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.street_name

class CityName(models.Model):
    city_name = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('city_name'),
                name='uniq_city_name_ci'
            )
        ]
    def save(self, *args, **kwargs):
        if self.city_name:
            self.city_name = self.city_name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.city_name

class District(models.Model):
    district_name = models.ForeignKey(DistrictName, on_delete=models.PROTECT)
    post_code = models.ForeignKey(PostCode, on_delete=models.PROTECT)
    city = models.ForeignKey(CityName, on_delete=models.PROTECT)
    street = models.ForeignKey(StreetName, on_delete=models.PROTECT, blank=True, null=True)
    signed_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='signed_user')

    def __str__(self):
        return f' {self.post_code} osiedle {self.district_name}'

class ParkingPlaceData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    place_number = models.CharField(default=1)
    available_from = models.DateTimeField(default=timezone.now)
    available_until = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.district.district_name} - {self.place_number}'








