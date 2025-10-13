from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from parking_place.forms import DistrictForm, DistrictNameForm
from parking_place.models import District


# Create your views here.
def map_view(request):
    return render(request, 'map_view.html')


class AddNewDistrictView(LoginRequiredMixin, View):
    def post(self, request):
        add_district_name_form = DistrictNameForm(request.POST)

        if add_district_name_form.is_valid():
            add_district_name_form.save()
            return redirect('user_account')


class AddUserToDistrictView(View):
    def post(self, request):
        add_user_to_district_form = DistrictForm(request.POST)
        if add_user_to_district_form.is_valid():
            district = add_user_to_district_form.save(commit=False)
            district.save()
            district.signed_user.add(request.user)
            messages.success(request, f'You have successfully joined osiedle {district.district_name}')
            return redirect('user_account')


class PlaceListView(View):
    def get(self, request):
        places = District.objects.all()
        url = 'place_list'
        return render(request, 'account_form.html', {
            'places': places,
            'url': url
        })
class PlaceDetailView(View):
    def get(self, request, pk):
        place = District.objects.get(pk=pk)
        return render(request, 'place_detail.html', {
            'place': place,
            'pk': pk
        })