from rest_framework import serializers

class ListCryptoCurrensySerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10)
    sparkline = serializers.BooleanField(default=False)

    # def list