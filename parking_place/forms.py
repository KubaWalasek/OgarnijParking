from django import forms
from .models import District, DistrictName, ParkingPlaceData


class DistrictNameForm(forms.ModelForm):
    class Meta:
        model = DistrictName
        fields = ('district_name',)
        widgets = {'district_name': forms.TextInput(attrs={'placeholder': 'Nazwa osiedla'})}

    def clean_district_name(self):
        district_name_cleaned = self.cleaned_data['district_name']
        district_name = district_name_cleaned.strip().title()
        if DistrictName.objects.filter(district_name=district_name).exists():
            raise forms.ValidationError('Osiedle o podanej nazwie już istnieje.')
        return district_name


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district_name']
        widgets = {'district_name': forms.Select()}

class ParkingPlaceDataForm(forms.ModelForm):
    class Meta:
        model = ParkingPlaceData
        fields = ['place_number', 'available_from', 'available_until', 'description']