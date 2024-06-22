from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from basic_info.models import CryptoCurrency
from . import serializers


class ListCryptoCurrensy(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.ListCryptoCurrensySerializer
    queryset = CryptoCurrency.objects.filter(is_active=True).order_by('created_at')

class SwapCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapCryptoCurrensySerializer

class SwapDollarCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapDollarCryptoCurrensySerializer

from django.shortcuts import render

def crypto_dashboard(request):
    return render(request, 'crypto_dashboard.html')
