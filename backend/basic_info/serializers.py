from rest_framework import serializers
from .models import Country, City 


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        extra_kwargs = {
            'is_show': {'default': True},
        }

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        extra_kwargs = {
            'is_show': {'default': True},
        }

# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = '__all__'