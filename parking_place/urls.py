from django.urls import path

from parking.views import map_view

urlpatterns = [
    path('map/', map_view, name='map_view'),
]