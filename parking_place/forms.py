from django import forms
from .models import District,  ParkingPlaceData, PostCode, StreetName, CityName


class PostCodeForm(forms.ModelForm):
    class Meta:
        model = PostCode
        fields = ('post_code',)
        widgets = {'post_code': forms.TextInput(attrs={'placeholder': 'Kod pocztowy'})}


class StreetNameForm(forms.ModelForm):
    street_name = forms.CharField(required=False)
    class Meta:
        model = StreetName
        fields = ('street_name',)
        widgets = {'street_name': forms.TextInput(attrs={'placeholder': 'Ulica'})}


class CityNameForm(forms.ModelForm):
    class Meta:
        model = CityName
        fields = ('city_name',)
        widgets = {'city_name': forms.TextInput(attrs={'placeholder': 'Miasto'})}


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('district_name', 'city_name', 'street_name', 'post_code')
        widgets = {
            'district_name': forms.TextInput(attrs={'placeholder': 'Osiedle'}),
            'post_code': forms.Select(),
            'city_name': forms.Select(),
            'street_name': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street_name'].required = False
        self.fields['street_name'].empty_label = '— brak ulicy —'


class ParkingPlaceDataForm(forms.ModelForm):
    class Meta:
        model = ParkingPlaceData
        fields = ('place_number', 'available_from', 'available_until', 'description')

class AddUserToDistrictForm(forms.Form):
       selected_districts = forms.ModelMultipleChoiceField(
           queryset=District.objects.all(),
           widget=forms.CheckboxSelectMultiple,
           required=True
       )


class DistrictSearchForm(forms.Form):
    district_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Osiedle'}), required=False)
    city_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Miasto'}), required=False)
    street_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Ulica'}), required=False)
    post_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Kod pocztowy'}), required=False)