from rest_framework import serializers
from pycoingecko import CoinGeckoAPI
from .models import CryptoCurrency
from utils.response import CustomValidationError
from django.utils.translation import gettext as _

class ListCryptoCurrensySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ['coin_id', 'coin_name', 'coin_symbol', 'coin_image']

class SwapCryptoCurrensySerializer(serializers.Serializer):
    coin1 = serializers.CharField(max_length=100)
    coin2 = serializers.CharField(max_length=100)
    number_of_coin1 = serializers.FloatField()
    number_of_coin2 = serializers.FloatField(read_only=True)

    def validate(self, attrs):
        cg = CoinGeckoAPI()
        if cg.get_price(ids=attrs['coin1'], vs_currencies='usd') == {} or cg.get_price(ids=attrs['coin2'], vs_currencies='usd') == {}:
            raise CustomValidationError(_('No currency was found with this information.'))

        return attrs

    def save(self, **kwargs):
        cg = CoinGeckoAPI()
        get_coin1_price = cg.get_price(ids=self.validated_data['coin1'], vs_currencies='usd')
        get_coin2_price = cg.get_price(ids=self.validated_data['coin2'], vs_currencies='usd')
        total_price_coin1 = get_coin1_price[self.validated_data['coin1']]['usd'] * self.validated_data['number_of_coin1']
        self.validated_data['number_of_coin2'] = total_price_coin1 / get_coin2_price[self.validated_data['coin2']]['usd']

        return self.validated_data


class SwapDollarCryptoCurrensySerializer(serializers.Serializer):
    coin = serializers.CharField(max_length=100)
    number_of_coin = serializers.FloatField(default=0)
    dollar = serializers.FloatField(default=0)

    def validate(self, attrs):
        if attrs['number_of_coin'] == 0 and attrs['dollar'] == 0:
            raise CustomValidationError(_('Please submit the number_of_coin or dollar field.'))

        elif attrs['number_of_coin'] != 0 and attrs['dollar'] != 0:
            raise CustomValidationError(_('Please submit only one item between the number_of_coin and dollar fields.'))

        return attrs

    def save(self, **kwargs):
        cg = CoinGeckoAPI()
        get_coin_price = cg.get_price(ids=self.validated_data['coin'], vs_currencies='usd')[self.validated_data['coin']]['usd']
        
        if self.validated_data['number_of_coin'] != 0:
            self.validated_data['dollar'] = get_coin_price * self.validated_data['number_of_coin']
        else:
            self.validated_data['number_of_coin'] = self.validated_data['dollar'] / get_coin_price

        return self.validated_data

