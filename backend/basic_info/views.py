# Create your views here.

from rest_framework import viewsets
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer
from .permissions import IsSuperuser
from .filters import CityFilter , CountryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    ordering_fields = ['title']
    search_fields = ['title']


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']

class CountryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    ordering_fields = ['title']
    search_fields = ['title']

class CityReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']
