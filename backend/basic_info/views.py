# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets
from .models import Country, City, State
from .serializers import CountrySerializer, CitySerializer, StateSerializer


class CountryViewSetApiView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSetApiView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StateViewSetApiView(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer