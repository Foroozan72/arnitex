from rest_framework import serializers
from pycoingecko import CoinGeckoAPI
from basic_info.models import CryptoCurrency

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
            raise serializers.ValidationError("Sending one of the number_of_coin and dollar fields is required.")

        elif attrs['number_of_coin'] != 0 and attrs['dollar'] != 0:
            raise serializers.ValidationError("Please send only one between the number_of_coin and dollar fields.")

        return attrs

    def save(self, **kwargs):
        cg = CoinGeckoAPI()
        get_coin_price = cg.get_price(ids=self.validated_data['coin'], vs_currencies='usd')[self.validated_data['coin']]['usd']
        
        if self.validated_data['number_of_coin'] != 0:
            self.validated_data['dollar'] = get_coin_price * self.validated_data['number_of_coin']
        else:
            self.validated_data['number_of_coin'] = self.validated_data['dollar'] / get_coin_price

        return self.validated_data

