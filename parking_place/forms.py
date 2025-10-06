from django import forms
from parking.models import ParkingPlace


class ParkingPlaceForm(forms.ModelForm):
    class Meta:
        model = ParkingPlace
        fields = (
            'place_name',
            'city',
            'post_code',
            'district_name',
            'estate_name',
            'street_name',
            'street_number',
            'place_number',
            'description',
            'longitude',
            'latitude',

        )
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }