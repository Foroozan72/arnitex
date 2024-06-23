from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Country, City , Wallet
from .serializers import CountrySerializer, CitySerializer , WalletSerializer
from .permissions import IsSuperuser
from .filters import CityFilter , CountryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import qrcode
from io import BytesIO
from django.core.files import File
from rest_framework.response import Response
from pywalletconnectv1.wc_client import WCClient  
from pywalletconnectv1.models.session.wc_session import WCSession
from pywalletconnectv1.models.wc_peer_meta import WCPeerMeta


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
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CountryFilter
    ordering_fields = ['title']
    search_fields = ['title']

class CityReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CityFilter
    ordering_fields = ['title']
    search_fields = ['title']

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    #permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['wallet_name']
    search_fields = ['wallet_name', 'description']

    def create(self, request, *args, **kwargs):
        wc = WCClient()  
        qrcode_data = wc.connect()  

        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrcode_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        
        wallet = Wallet(
            wallet_id=request.data.get('wallet_id'),
            wallet_name=request.data.get('wallet_name'),
            description=request.data.get('description'),
            website_url=request.data.get('website_url'),
            is_active=request.data.get('is_active', True),
            logo=request.data.get('logo')
        )
        
        
        wallet.qr_code.save(f"wallet_{wallet.wallet_id}_qrcode.png", File(buffer), save=True)
        wallet.save()

        serializer = WalletSerializer(wallet)
        return Response(serializer.data)