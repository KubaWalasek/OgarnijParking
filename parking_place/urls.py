from django.urls import path

from parking_place.views import map_view, AddUserToDistrictView, AddNewDistrictView, PlaceDetailView, PlaceListView

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('add_to_district/', AddUserToDistrictView.as_view(), name='add_to_district'),
    path('add_new_district/', AddNewDistrictView.as_view(), name='add_new_district'),
    path('place_list/', PlaceListView.as_view(), name='place_list'),
    path('place_detail/<int:pk>/', PlaceDetailView.as_view(), name='place_detail')

]