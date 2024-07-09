from decimal import Decimal
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import viewsets, status, filters

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils import translation

from .models import Asset, BankAccount
from . import serializers
from utils.response import APIResponse, APIResponseMixin, CustomPagination
from utils.classes import get_tether_price, crypto_currency_inf
from crypto_currency.models import CryptoCurrency
User = get_user_model()



####  BANK ACCOUNTS  ####
class AddBankAccount(APIResponseMixin, CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.AddBankAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(msg=_('The bank account was created successfully.'), data=serializer.data)

class BankAccountViewSet(APIResponseMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.BankAccountsSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    pagination_class = CustomPagination
    ordering_fields = ['-created_at']
    search_fields = ['BIN', 'IBAN', 'bank_account']

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.api_response(msg=_('The bank account was deleted.'))

####  ASSET  ####
class TotalAsset(APIResponseMixin, ListModelMixin, viewsets.GenericViewSet):
    def get_tether_price_toman(self, price):
        str_price = str(price)
        str_price = str_price[:-1]

        return float(str_price)
    
    def get_tether(self):
        tether_id = '825'
        inf_coin = crypto_currency_inf(tether_id)
        tether_price = inf_coin[tether_id]['quote']['USD']['price']
        return float(f"{tether_price:.3f}")

    def list(self, request, *args, **kwargs):
        tether_price = get_tether_price()
        tether_price_rial = (tether_price['buy'] + tether_price['sell']) / 2
        tether_price_toman = self.get_tether_price_toman(int(tether_price_rial))

        assets_user = Asset.objects.filter(user=request.user)
        asset_toman = 0
        asset_tether = 0

        for i in assets_user:
            if i.coin.coin_name == 'Toman':
                asset_toman += float(i.amount)
                asset_tether += float(i.amount) / tether_price_toman
            else:
                inf_coin = crypto_currency_inf(i.coin.coin_id)
                asset_toman += (float(i.amount) * inf_coin[i.coin.coin_id]['quote']['USD']['price']) * tether_price_toman
                print(float(i.amount) * inf_coin[i.coin.coin_id]['quote']['USD']['price'])
                asset_tether += (float(i.amount) * inf_coin[i.coin.coin_id]['quote']['USD']['price']) / self.get_tether()

        return self.api_response(data={"asset_toman": asset_toman, "asset_tether": asset_tether})
