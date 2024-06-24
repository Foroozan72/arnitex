from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Country, City, Wallet
from .serializers import CountrySerializer, CitySerializer
from .permissions import IsSuperuser
from .filters import CityFilter, CountryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import qrcode
from io import BytesIO
from django.core.files import File
from rest_framework.response import Response
from pywalletconnectv1.wc_client import WCClient

class CountryViewSet(viewsets.ModelViewSet):
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
    ordering_fields = ['title']
    search_fields = ['title']


class CityViewSet(viewsets.ModelViewSet):
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


class CountryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
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
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    ordering_fields = ['title']
    search_fields = ['title']


class CityReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
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
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']


# class WalletViewSet(viewsets.ModelViewSet):
   
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     filterset_fields = ['is_active']
#     ordering_fields = ['wallet_name']
#     search_fields = ['wallet_name', 'description']

#     def create(self, request, *args, **kwargs):
#         wc = WCClient()  
#         qrcode_data = wc.connect()  

#         # Create QR Code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qrcode_data)
#         qr.make(fit=True)

#         img = qr.make_image(fill='black', back_color='white')

#         # Save QR Code to a file-like object
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)

#         # Create and save Wallet object
#         wallet = Wallet(
#             wallet_id=request.data.get('wallet_id'),
#             wallet_name=request.data.get('wallet_name'),
#             description=request.data.get('description'),
#             website_url=request.data.get('website_url'),
#             is_active=request.data.get('is_active', True),
#             logo=request.data.get('logo')
#         )
        
#         # Attach QR Code image to the Wallet object
#         wallet.qr_code.save(f"wallet_{wallet.wallet_id}_qrcode.png", File(buffer), save=True)
#         wallet.save()

#         serializer = WalletSerializer(wallet)
#         return Response(serializer.data)
