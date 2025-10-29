from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from parking_place.forms import DistrictForm, PostCodeForm, StreetNameForm, CityNameForm, \
    ParkingPlaceForm, AddUserToDistrictForm, DistrictSearchForm, UserDistrictsForm, ShareParkingPlaceForm, \
    UserParkingPlacesForm
from parking_place.models import District, PostCode, CityName, StreetName, ParkingPlace, ValidityPeriod


def map_view(request):
    return render(request, 'map_view.html')

class MyPlaceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        districts = District.objects.filter(signed_user=user)
        places = ParkingPlace.objects.filter(owner=user)
        user_districts_form = UserDistrictsForm(user=user)
        user_parking_places_form = UserParkingPlacesForm(user=user)

        return render(request, 'my_places.html', {
            'url': 'user_account',
            'districts': districts,
            'user_districts_form': user_districts_form,
            'user_parking_places_form': user_parking_places_form,
            'places': places,
        })

    def post(self, request, pk):
        user = request.user
        add_user_to_district_form = DistrictForm(request.POST)
        user_districts_form = UserDistrictsForm(request.POST, user=user)
        user_parking_places_form = UserParkingPlacesForm(request.POST, user=user)

        if 'add_parking' in request.POST:
            if not District.objects.filter(signed_user=user).exists():
                messages.error(request, 'Dołącz do osiedla aby móc dodać miejsce parkingowe!')
                return redirect('my_place', pk=user.pk)
            if user_districts_form.is_valid():
                district = user_districts_form.cleaned_data['district']
                return redirect('add_parking_place', pk=district.pk)

        elif 'share_parking' in request.POST:
            if not ParkingPlace.objects.filter(owner=user).exists():
                messages.error(request, 'Musisz najpierw dodać miejsce parkingowe!')
                return redirect('my_place', pk=user.pk)
            if user_parking_places_form.is_valid():
                place = user_parking_places_form.cleaned_data['place']
                return redirect('share_parking_place', pk=place.pk)
        return render(request, 'account_form.html', {
            'add_user_to_district_form': add_user_to_district_form,
        })


class PlaceListView(View):
    def get(self, request):
        districts = District.objects.all()
        return render(request, 'place_list.html', {
            'districts': districts,
        })


class PlaceValidityView(LoginRequiredMixin, View):
    def get(self, request, pk):
        district = District.objects.get(pk=pk)
        validities = (ValidityPeriod.objects.filter(
            parking_place__district=district,is_reserved=False)
                      .select_related('parking_place'))
        return render(request, 'place_validity_list.html', {
            'district': district,
            'validities': validities,
        })

    def post(self, request, pk):

        if 'reserve' in request.POST:
            validity_id = request.POST.get('reserve')
            validity = ValidityPeriod.objects.get(pk=validity_id)
            validity.is_reserved = True

            validity.save()
            messages.success(request, 'Place reserved successfully!')
            return redirect('my_place', pk=request.user.pk)


class AddUserToDistrictPkView(View):
    def post(self, request,pk):
        district = District.objects.get(pk=pk)
        if not district.signed_user.filter(pk=request.user.pk).exists():
            district.signed_user.add(request.user)
            messages.success(request, 'User added successfully!')
            return redirect('district')
        messages.error(request, 'You already joined this district!')
        return redirect('district')


class DistrictView(LoginRequiredMixin, View):
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

class AddUserToDistrictView(LoginRequiredMixin, View):
    def post(self, request):
        add_user_to_district_form = AddUserToDistrictForm(request.POST)
        if add_user_to_district_form.is_valid():
            selected_districts = add_user_to_district_form.cleaned_data['selected_districts']
            for district in selected_districts:
                if not district.signed_user.filter(pk=request.user.pk).exists():
                    district.signed_user.add(request.user)
                    messages.success(request, 'User added successfully!')
                else:
                    messages.error(request, 'You already joined this district!')
            return redirect('district')
        else:
            messages.error(request, 'No data selected.')
            return redirect('district')

class RemoveUserFromDistrictView(LoginRequiredMixin, View):
    def post(self, request):
        add_user_to_district_form = AddUserToDistrictForm(request.POST)
        if add_user_to_district_form.is_valid():
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
            return redirect('district')


class AddDistrictView(LoginRequiredMixin, View):
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


class AddPostCodeView(LoginRequiredMixin, View):

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

class AddStreetNameView(LoginRequiredMixin, View):

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


class AddCityNameView(LoginRequiredMixin, View):

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

class CreateDistrictView(LoginRequiredMixin, View):
    def post(self, request):
        create_district_form = DistrictForm(request.POST)
        if create_district_form.is_valid():
            create_district_form.save()
            messages.success(request, 'District created successfully!')
            return redirect('add_district')
        messages.error(request, 'Invalid district data!')
        return redirect('add_district')

class AddParkingPlaceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        add_parking_place_form = ParkingPlaceForm()
        district = District.objects.get(pk=pk)
        return render(request, 'parking_place.html',{
            'add_parking_place_form': add_parking_place_form,
            'pk':pk,
            'district':district,
        })

    def post(self, request, pk):
        user = request.user
        add_parking_place_form = ParkingPlaceForm(request.POST)
        district = District.objects.get(pk=pk)
        if add_parking_place_form.is_valid():
            parking_place = add_parking_place_form.save(commit=False)
            parking_place.owner = user
            parking_place.district = district
            parking_place.save()
            messages.success(request, 'Parking place added successfully!')
            return redirect('my_place', pk=user.pk)
        messages.error(request, 'Invalid parking place data!')
        return redirect('my_place', pk=user.pk)


class ShareParkingPlaceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        share_parking_place_form = ShareParkingPlaceForm()
        place = ParkingPlace.objects.get(pk=pk)
        return render(request, 'share_parking_place.html',{
            'share_parking_place_form': share_parking_place_form,
            'pk':pk,
            'place':place,
        })

    def post(self, request, pk):
        share_parking_place_form = ShareParkingPlaceForm(request.POST)
        place = ParkingPlace.objects.get(pk=pk)
        if share_parking_place_form.is_valid():
            shared_parking_place = share_parking_place_form.save(commit=False)
            shared_parking_place.parking_place = place
            shared_parking_place.save()
            messages.success(request, 'Parking place shared successfully!')
            return redirect('my_place', pk=request.user.pk)
        messages.error(request, 'Invalid parking place data!')
        return redirect('my_place', pk=request.user.pk)



















