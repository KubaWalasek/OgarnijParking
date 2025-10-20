from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from parking_place.forms import DistrictForm, PostCodeForm, StreetNameForm, CityNameForm, \
    ParkingPlaceDataForm, AddUserToDistrictForm, DistrictSearchForm
from parking_place.models import District, PostCode, CityName, StreetName


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


class AddUserToDistrictPkView(View):
    def post(self, request,pk):
        district = District.objects.get(pk=pk)
        if not district.signed_user.filter(pk=request.user.pk).exists():
            district.signed_user.add(request.user)
            messages.success(request, 'User added successfully!')
            return redirect('district')
        messages.error(request, 'You already joined this district!')
        return redirect('district')


class DistrictView(View):
    def get(self, request):
        add_user_to_district_form = AddUserToDistrictForm()
        district_search_form = DistrictSearchForm(request.GET or None)
        districts = District.objects.all()
        if district_search_form.is_valid():
            district_name = (district_search_form.cleaned_data.get('district_name') or '').strip()
            city_name = (district_search_form.cleaned_data.get('city_name') or '').strip()
            street_name = (district_search_form.cleaned_data.get('street_name') or '').strip()
            post_code = (district_search_form.cleaned_data.get('post_code') or '').strip()

            if district_name:
                districts = districts.filter(district_name__icontains=district_name)
            if city_name:
                districts = districts.filter(city_name__city_name__icontains=city_name)
            if street_name:
                districts = districts.filter(street_name__street_name__icontains=street_name)
            if post_code:
                districts = districts.filter(post_code__post_code__icontains=post_code)

        add_user_to_district_form.fields['selected_districts'].queryset = districts

        return render(request, 'district.html', {
            'add_user_to_district_form': add_user_to_district_form,
            'district_search_form': district_search_form,
            'districts': districts,
        })

class AddOrRemoveUserFromDistrictView(View):
    def post(self, request):
        action = request.POST.get('action')
        add_user_to_district_form = AddUserToDistrictForm(request.POST)
        if add_user_to_district_form.is_valid():
            if action =='add':
                selected_districts = add_user_to_district_form.cleaned_data['selected_districts']
                for district in selected_districts:
                    if not district.signed_user.filter(pk=request.user.pk).exists():
                        district.signed_user.add(request.user)
                        messages.success(request, 'User added successfully!')
                    else:
                        messages.error(request, 'You already joined this district!')
                return redirect('district')
            elif action == 'remove':
                selected_districts = add_user_to_district_form.cleaned_data['selected_districts']
                for district in selected_districts:
                    if district.signed_user.filter(pk=request.user.pk).exists():
                        district.signed_user.remove(request.user)
                        messages.success(request, 'User removed successfully!')
                    else:
                        messages.error(request, 'You are not joined this district!')
                return redirect('district')
            else:
                messages.error(request, 'No data selected.')



class AddDistrictView(View):
    def get(self, request):
        add_post_code_form = PostCodeForm()
        add_street_name_form = StreetNameForm()
        add_city_name_form = CityNameForm()
        create_district_form = DistrictForm()

        return render(request, 'add_district.html', {
            'add_post_code_form': add_post_code_form,
            'add_street_name_form': add_street_name_form,
            'add_city_name_form': add_city_name_form,
            'create_district_form': create_district_form,
        })


class ParkingPlaceView(View):
    def get(self, request):
        add_parking_place_form = ParkingPlaceDataForm()
        return render(request, 'parking_place.html', {
            'add_parking_place_form': add_parking_place_form,
        })



class AddPostCodeView(View):

    def post(self, request):
        add_post_code_form = PostCodeForm(request.POST)
        if add_post_code_form.is_valid():
            post_code = add_post_code_form.cleaned_data['post_code']
            if PostCode.objects.filter(post_code=post_code).exists():
                messages.error(request, 'Post code already exists!')
                return redirect('add_district')
            add_post_code_form.save()
            messages.success(request, 'Post code added successfully!')
            return redirect('add_district')
        messages.error(request, 'Invalid post code!')
        return redirect('add_district')

class AddStreetNameView(View):

    def post(self, request):
        add_street_name_form = StreetNameForm(request.POST)
        if add_street_name_form.is_valid():
            street_name = add_street_name_form.cleaned_data['street_name']
            if StreetName.objects.filter(street_name=street_name).exists():
                messages.error(request, 'Street name already exists!')
                return redirect('add_district')
            add_street_name_form.save()
            messages.success(request, 'Street name added successfully!')
            return redirect('add_district')
        messages.error(request, 'Invalid street name!')
        return redirect('add_district')


class AddCityNameView(View):

    def post(self, request):
        add_city_name_form = CityNameForm(request.POST)
        if add_city_name_form.is_valid():
            city_name = add_city_name_form.cleaned_data['city_name']
            if CityName.objects.filter(city_name=city_name).exists():
                messages.error(request, 'City name already exists!')
                return redirect('add_district')
            add_city_name_form.save()
            messages.success(request, 'City name added successfully!')
            return redirect('add_district')
        return redirect('add_district')

class CreateDistrictView(View):

    def post(self, request):
        create_district_form = DistrictForm(request.POST)
        if create_district_form.is_valid():
            create_district_form.save()
            messages.success(request, 'District created successfully!')
            return redirect('add_district')
        messages.error(request, 'Invalid district data!')
        return redirect('add_district')

class AddParkingPlaceView(View):

    def post(self, request):
        add_parking_place_form = ParkingPlaceDataForm(request.POST)
        if add_parking_place_form.is_valid():
            add_parking_place_form.save()
            messages.success(request, 'Parking place added successfully!')
            return redirect('parking_place')
        messages.error(request, 'Invalid parking place data!')
        return redirect('parking_place')






















