from rest_framework import serializers
from .models import Country  , City , State




class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'     





class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only = True , many = True)

    state = StateSerializer(read_only = True , many = True)

    class Meta:
        model = City
        fields = '__all__'