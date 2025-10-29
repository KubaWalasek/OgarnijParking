from django import forms
from .models import District, ParkingPlace, PostCode, StreetName, CityName, ValidityPeriod


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


class ParkingPlaceForm(forms.ModelForm):
    class Meta:
        model = ParkingPlace
        fields = ('place_number', 'description')

class ShareParkingPlaceForm(forms.ModelForm):
    class Meta:
        model = ValidityPeriod
        fields = ('available_from', 'available_until')
        widgets = {
            'available_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'available_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AddUserToDistrictForm(forms.Form):
       selected_districts = forms.ModelMultipleChoiceField(
           queryset=District.objects.all(),
           widget=forms.CheckboxSelectMultiple,
           required=True
       )

class UserDistrictsForm(forms.Form):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label= '',
        widget=forms.RadioSelect(),
        required=True
        )
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            district_qs = District.objects.filter(signed_user=user)
            self.fields['district'].queryset = district_qs
            if not district_qs.exists():
                self.fields['district'].empty_label = '-brak zapisanych osiedli - dołącz do osiedla aby móc dodać miejsce parkingowe-'


class UserParkingPlacesForm(forms.Form):
    place = forms.ModelChoiceField(
        queryset=ParkingPlace.objects.all(),
        label= '',
        widget=forms.RadioSelect(),
        required=True
        )
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            place_qs = ParkingPlace.objects.filter(owner=user)
            self.fields['place'].queryset = place_qs
            if not place_qs.exists():
                self.fields['place'].empty_label = '-brak zapisanych miejsc - dodaj miejsce parkingowe, aby móc je udostępnić-'



class DistrictSearchForm(forms.Form):
    district_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Osiedle'}), required=False)
    city_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Miasto'}), required=False)
    street_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Ulica'}), required=False)
    post_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Kod pocztowy'}), required=False)