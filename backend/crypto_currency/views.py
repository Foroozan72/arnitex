from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from django.utils.translation import gettext as _

from .models import CryptoCurrency
from utils.response import APIResponseMixin
from . import serializers


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


class SwapCryptoCurrensy(APIResponseMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to handle the swapping of cryptocurrencies.

    Methods:
    - create(request, *args, **kwargs): Handles POST requests to swap cryptocurrencies.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapCryptoCurrensySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(data=serializer.data)


class SwapDollarCryptoCurrensy(APIResponseMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to handle the swapping of dollars to cryptocurrencies.

    Methods:
    - create(request, *args, **kwargs): Handles POST requests to swap dollars to cryptocurrencies.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    serializer_class = serializers.SwapDollarCryptoCurrensySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(data=serializer.data)


def crypto_dashboard(request):
    """
    View function to render the cryptocurrency dashboard.

    Permissions:
    - AllowAny: No authentication required.
    """
    return render(request, 'crypto_dashboard.html')


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from coinmarketcapapi import CoinMarketCapAPI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
import datetime
import numpy as np

CoinMarketCap_API_KEY = os.environ.get("CoinMarketCap_API_KEY")
cmc = CoinMarketCapAPI(CoinMarketCap_API_KEY)


def generate_chart_image(weekly_data):
    dates = [data[0] for data in weekly_data]
    prices = [data[1] for data in weekly_data]

    # استفاده از میانگین متحرک برای صاف کردن داده‌ها
    window_size = 3
    prices_smooth = np.convolve(prices, np.ones(window_size) / window_size, mode='valid')
    dates_smooth = dates[window_size - 1:]

    if prices_smooth[-1] >= prices_smooth[0]:
        line_color = 'green'
    else:
        line_color = 'red'

    fig, ax = plt.subplots()
    ax.plot(dates_smooth, prices_smooth, color=line_color, linewidth=1.5)

    price_range = max(prices_smooth) - min(prices_smooth)
    if price_range == 0:
        min_price, max_price = min(prices_smooth) * 0.99, max(prices_smooth) * 1.01
    else:
        min_price, max_price = min(prices_smooth) - price_range * 0.1, max(prices_smooth) + price_range * 0.1
    ax.set_ylim(min_price, max_price)

    ax.set_facecolor('white')
    ax.axis('off')

    fig.set_size_inches(3, 1.5)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return image_base64

class CryptoChartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'])
    def get_charts(self, request):
        coin_ids = request.data.get('coin_ids', [])
        charts = {}

        for coin_id in coin_ids:
            end_date = datetime.datetime.utcnow()
            start_date = end_date - datetime.timedelta(days=7)
            response = cmc.cryptocurrency_quotes_historical(
                id=coin_id,
                convert='USD',
                time_start=start_date.isoformat(),
                time_end=end_date.isoformat()
            )

            if 'quotes' in response.data:
                historical_data = response.data['quotes']
                weekly_data = [(quote['timestamp'], quote['quote']['USD']['price']) for quote in historical_data]
                charts[coin_id] = generate_chart_image(weekly_data)
            else:
                charts[coin_id] = None

        return Response(charts)

def chart_view(request):
    return render(request, 'chart_view.html')