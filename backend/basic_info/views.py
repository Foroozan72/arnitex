from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _

from .models import Country, City
from .serializers import CountrySerializer, CitySerializer
from .filters import CityFilter, CountryFilter
from .permissions import IsSuperuser
from utils.response import APIResponse, APIResponseMixin, CustomPagination


import qrcode
from io import BytesIO
from django.core.files import File
from rest_framework.response import Response
from pywalletconnectv1.wc_client import WCClient

class CountryViewSet(APIResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing Country objects.
    
    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all countries.
    - create(request, *args, **kwargs): Creates a new country.
    - retrieve(request, *args, **kwargs): Retrieves a country by its ID.
    - update(request, *args, **kwargs): Updates an existing country.
    - partial_update(request, *args, **kwargs): Partially updates an existing country.
    - destroy(request, *args, **kwargs): Deletes a country by its ID.
    
    Inputs:
    - request: The HTTP request containing necessary data for the respective actions.
    
    Outputs:
    - response: JSON response with the details of the country or a list of countries.
    
    Permissions:
    - IsSuperuser: Requires the user to be a superuser.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    pagination_class = CustomPagination
    ordering_fields = ['title']
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(msg=_('The country was created successfully.'), data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.api_response(msg=_('The country was updated successfully.'), data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.api_response(msg=_('The country was deleted.'))


class CityViewSet(APIResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing City objects.
    
    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all cities.
    - create(request, *args, **kwargs): Creates a new city.
    - retrieve(request, *args, **kwargs): Retrieves a city by its ID.
    - update(request, *args, **kwargs): Updates an existing city.
    - partial_update(request, *args, **kwargs): Partially updates an existing city.
    - destroy(request, *args, **kwargs): Deletes a city by its ID.
       
    Permissions:
    - IsSuperuser: Requires the user to be a superuser.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(msg=_('The city created successfully.'), data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.api_response(msg=_('The city was updated successfully.'), data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.api_response(msg=_('The city was deleted.'))


class CountryReadOnlyViewSet(APIResponseMixin, viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for viewing Country objects.
    
    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all countries.
    - retrieve(request, *args, **kwargs): Retrieves a country by its ID.
    
    Inputs:
    - request: The HTTP request containing necessary data for the respective actions.
    
    Outputs:
    - response: JSON response with the details of the country or a list of countries.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    queryset = Country.objects.filter(is_show=True)
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    ordering_fields = ['title']
    search_fields = ['title']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)


class CityReadOnlyViewSet(APIResponseMixin, viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for viewing City objects.
    
    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all cities.
    - retrieve(request, *args, **kwargs): Retrieves a city by its ID.
    
    Inputs:
    - request: The HTTP request containing necessary data for the respective actions.
    
    Outputs:
    - response: JSON response with the details of the city or a list of cities.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    queryset = City.objects.filter(is_show=True)
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)