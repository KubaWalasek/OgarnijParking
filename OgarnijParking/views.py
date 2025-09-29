from django.conf import settings
from django.contrib.sites import requests
from django.shortcuts import render


def home(request):
    return render(request, 'base.html')