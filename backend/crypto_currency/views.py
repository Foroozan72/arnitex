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
        crypto_list = APICryptoCurrency.crypto_currencies(limit=limit, sparkline=sparkline)
        crypto_data = []
        for crypto in crypto_list:
            if sparkline:
                crypto_data.append({
                    "name": crypto['name'], 
                    "symbol": crypto['symbol'], 
                    "current_price": crypto['current_price'], 
                    "ath_change_percentage": crypto['ath_change_percentage'], 
                    "market_cap": crypto['market_cap'], 
                    "total_volume": crypto['total_volume'], 
                    "sparkline_in_7d": crypto['sparkline_in_7d']['price'], 
                    "image": crypto['image'], 
                })
            else:
                crypto_data.append({
                    "name": crypto['name'], 
                    "symbol": crypto['symbol'], 
                    "current_price": crypto['current_price'], 
                    "ath_change_percentage": crypto['ath_change_percentage'], 
                    "market_cap": crypto['market_cap'], 
                    "total_volume": crypto['total_volume'], 
                    "image": crypto['image'], 
                })

        return Response({'data': crypto_data})