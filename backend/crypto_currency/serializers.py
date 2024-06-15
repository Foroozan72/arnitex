from rest_framework import serializers

class ListCryptoCurrensySerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10)

    # def list