from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from parking_place.forms import DistrictForm, PostCodeForm, StreetNameForm, CityNameForm, \
    ParkingPlaceDataForm, DistrictNameForm, AddUserToDistrictForm
from parking_place.models import District, DistrictName


# Create your views here.
def map_view(request):
    return render(request, 'map_view.html')


class PlaceListView(View):
    def get(self, request):
        places = District.objects.all()
        url = 'place_list'
        return render(request, 'account_form.html', {
            'places': places,
            'url': url
        })


class AddUserToDistrictView(View):
    def post(self, request):
        add_user_to_district_form = AddUserToDistrictForm(request.POST)
        if add_user_to_district_form.is_valid():
            district = add_user_to_district_form.cleaned_data['district']
            district.signed_user.add(request.user)
            district.save()
            messages.success(request, 'User added successfully!')
            return redirect('district')
        messages.error(request, 'Invalid data!')
        return redirect('district')



class DistrictView(View):
    def get(self, request):
        add_district_name_form = DistrictNameForm()
        add_post_code_form = PostCodeForm()
        add_street_name_form = StreetNameForm()
        add_city_name_form = CityNameForm()
        create_district_form = DistrictForm()
        add_user_to_district_form = AddUserToDistrictForm()


        return render(request, 'district.html', {
            'add_district_name_form': add_district_name_form,
            'add_post_code_form': add_post_code_form,
            'add_street_name_form': add_street_name_form,
            'add_city_name_form': add_city_name_form,
            'create_district_form': create_district_form,
            'add_user_to_district_form': add_user_to_district_form
        })


class ParkingPlaceView(View):
    def get(self, request):
        add_parking_place_form = ParkingPlaceDataForm()
        return render(request, 'parking_place.html', {
            'add_parking_place_form': add_parking_place_form,
        })


class AddDistrictNameView(View):

    def post(self, request):
        add_district_name_form = DistrictNameForm(request.POST)
        if add_district_name_form.is_valid():
            add_district_name_form.save()
            messages.success(request, 'District name added successfully!')
            return redirect('district')
        messages.error(request, 'Invalid data!')
        return redirect('district')

class AddPostCodeView(View):

    def post(self, request):
        add_post_code_form = PostCodeForm(request.POST)
        if add_post_code_form.is_valid():
            add_post_code_form.save()
            messages.success(request, 'Post code added successfully!')
            return redirect('district')
        messages.error(request, 'Invalid post code!')
        return redirect('district')

class AddStreetNameView(View):

    def post(self, request):
        add_street_name_form = StreetNameForm(request.POST)
        if add_street_name_form.is_valid():
            add_street_name_form.save()
            messages.success(request, 'Street name added successfully!')
            return redirect('district')
        messages.error(request, 'Invalid street name!')
        return redirect('district')


class AddCityNameView(View):

    def post(self, request):
        add_city_name_form = CityNameForm(request.POST)
        if add_city_name_form.is_valid():
            add_city_name_form.save()
            messages.success(request, 'City name added successfully!')
            return redirect('district')
        return redirect('district')

class CreateDistrictView(View):

    def post(self, request):
        create_district_form = DistrictForm(request.POST)
        if create_district_form.is_valid():
            create_district_form.save()
            messages.success(request, 'District created successfully!')
            return redirect('district')
        return redirect('district')

class AddParkingPlaceView(View):

    def post(self, request):
        add_parking_place_form = ParkingPlaceDataForm(request.POST)
        if add_parking_place_form.is_valid():
            add_parking_place_form.save()
            messages.success(request, 'Parking place added successfully!')
            return redirect('parking_place')
        messages.error(request, 'Invalid parking place data!')
        return redirect('parking_place')






















