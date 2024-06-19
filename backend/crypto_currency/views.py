from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import serializers
from utils.classes import APICryptoCurrency

class ListCryptoCurrensy(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.ListCryptoCurrensySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        limit = serializer.validated_data.get('limit')
        sparkline = serializer.validated_data.get('sparkline')
        crypto_list = APICryptoCurrency.crypto_currencies(limit=limit)
        crypto_data = []
        
        for crypto in crypto_list:
            if sparkline:
                crypto_data.append({
                    "id": crypto['ID'], 
                    "name": crypto['Name'], 
                    "symbol": crypto['Symbol'], 
                    "current_price": crypto['Current Price'], 
                    "24h_change": crypto['24h Change'], 
                    "24h_volume": crypto['24h Volume'], 
                    "market_cap": crypto['Market Cap'], 
                    "image": crypto['Image'], 
                    "weekly_chart": crypto['Weekly Chart'], 
                })
            else:
                crypto_data.append({
                    "id": crypto['ID'], 
                    "name": crypto['Name'], 
                    "symbol": crypto['Symbol'], 
                    "current_price": crypto['Current Price'], 
                    "24h_change": crypto['24h Change'], 
                    "24h_volume": crypto['24h Volume'], 
                    "market_cap": crypto['Market Cap'], 
                    "image": crypto['Image'], 
                })

        return Response({'data': crypto_data})

class SwapCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapCryptoCurrensySerializer


class SwapDollarCryptoCurrensy(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapDollarCryptoCurrensySerializer

