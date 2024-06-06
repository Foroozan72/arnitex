# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer
from .permissions import IsSuperuser


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSuperuser]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsSuperuser]


class CountryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
