# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer


class CountryViewSetApiView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSetApiView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

