from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from basic_info.models import CryptoCurrency
from . import serializers
from django.shortcuts import render


class ListCryptoCurrensy(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list all active cryptocurrencies.

    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all active cryptocurrencies.
    - retrieve(request, *args, **kwargs): Retrieves a cryptocurrency by its ID.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.ListCryptoCurrensySerializer
    queryset = CryptoCurrency.objects.filter(is_active=True).order_by('created_at')


class SwapCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to handle the swapping of cryptocurrencies.

    Methods:
    - create(request, *args, **kwargs): Handles POST requests to swap cryptocurrencies.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapCryptoCurrensySerializer


class SwapDollarCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to handle the swapping of dollars to cryptocurrencies.

    Methods:
    - create(request, *args, **kwargs): Handles POST requests to swap dollars to cryptocurrencies.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapDollarCryptoCurrensySerializer


def crypto_dashboard(request):
    """
    View function to render the cryptocurrency dashboard.

    Permissions:
    - AllowAny: No authentication required.
    """
    return render(request, 'crypto_dashboard.html')
