from rest_framework import serializers
from .models import Country, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    # cities = CitySerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = '__all__'
