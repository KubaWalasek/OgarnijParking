from django.urls import path

from parking_place.views import map_view, AddPostCodeView, \
    AddStreetNameView, AddCityNameView, CreateDistrictView, AddParkingPlaceView, DistrictView, ParkingPlaceView, \
    AddDistrictNameView, AddUserToDistrictView

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('parking_place/', ParkingPlaceView.as_view(), name='parking_place'),
    path('add_user_to_district/', AddUserToDistrictView.as_view(), name='add_user_to_district'),
    path('district/', DistrictView.as_view(), name='district'),
    path('add_post_code/', AddPostCodeView.as_view(), name='add_post_code'),
    path('add_district_name/', AddDistrictNameView.as_view(), name='add_district_name'),
    path('add_street_name/', AddStreetNameView.as_view(), name='add_street_name'),
    path('add_city_name/', AddCityNameView.as_view(), name='add_city'),
    path('create_district/', CreateDistrictView.as_view(), name='create_district'),
    path('add_parking_place/', AddParkingPlaceView.as_view(), name='add_parking_place')

]