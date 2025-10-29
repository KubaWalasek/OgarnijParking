from django.urls import path

from parking_place.views import map_view, AddPostCodeView, \
    AddStreetNameView, AddCityNameView, CreateDistrictView, AddParkingPlaceView, DistrictView, \
    AddDistrictView, AddUserToDistrictPkView, RemoveUserFromDistrictView, AddUserToDistrictView, MyPlaceView, \
    ShareParkingPlaceView, PlaceListView, PlaceValidityView

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('my_place/<int:pk>', MyPlaceView.as_view(), name='my_place'),
    path('place_list/', PlaceListView.as_view(), name='place_list'),
    path('place_validity_list/<int:pk>', PlaceValidityView.as_view(), name='place_validity_list'),
    path('add_user_to_district/', AddUserToDistrictView.as_view(), name='add_user_to_district'),
    path('remove_user_from_district/', RemoveUserFromDistrictView.as_view(), name='remove_user_from_district'),
    path('district/', DistrictView.as_view(), name='district'),
    path('district/<int:pk>', AddUserToDistrictPkView.as_view(), name='add_user_to_district_pk'),
    path('add_district/', AddDistrictView.as_view(), name='add_district'),
    path('add_post_code/', AddPostCodeView.as_view(), name='add_post_code'),
    path('add_street_name/', AddStreetNameView.as_view(), name='add_street_name'),
    path('add_city_name/', AddCityNameView.as_view(), name='add_city'),
    path('create_district/', CreateDistrictView.as_view(), name='create_district'),
    path('add_parking_place/<int:pk>', AddParkingPlaceView.as_view(), name='add_parking_place'),
    path('share_parking_place/<int:pk>', ShareParkingPlaceView.as_view(), name='share_parking_place'),
]