from django import forms
from .models import District,  ParkingPlaceData, PostCode, StreetName, CityName, DistrictName


class DistrictNameForm(forms.ModelForm):
    class Meta:
        model = DistrictName
        fields = ('district_name',)
        widgets = {'district_name': forms.TextInput(attrs={'placeholder': 'dzielnica'})}


class PostCodeForm(forms.ModelForm):
    class Meta:
        model = PostCode
        fields = ('post_code',)
        widgets = {'post_code': forms.TextInput(attrs={'placeholder': 'Kod pocztowy'})}



class StreetNameForm(forms.ModelForm):
    street_number = forms.CharField(required=False)
    class Meta:
        model = StreetName
        fields = ('street_name', 'street_number')
        widgets = {
            'street_name': forms.TextInput(attrs={'placeholder': 'Ulica'}),
            'street_number': forms.TextInput(attrs={'placeholder': 'Numer'})
            }



class CityNameForm(forms.ModelForm):
    class Meta:
        model = CityName
        fields = ('city_name',)
        widgets = {'city_name': forms.TextInput(attrs={'placeholder': 'Miasto'})}



class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('district_name', 'city', 'street', 'post_code')
        widgets = {
            'district_name': forms.Select(),
            'post_code': forms.Select(),
            'city': forms.Select(),
            'street': forms.Select(),
        }



class ParkingPlaceDataForm(forms.ModelForm):
    class Meta:
        model = ParkingPlaceData
        fields = ('place_number', 'available_from', 'available_until', 'description')

class AddUserToDistrictForm(forms.Form):

       district = forms.ModelChoiceField(queryset=District.objects.all())
