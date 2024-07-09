from rest_framework import serializers
from django.utils.translation import gettext as _
from django.utils import translation

from .models import Asset, BankAccount
from utils.response import CustomValidationError

class AddBankAccountSerializer(serializers.Serializer):
    BIN = serializers.CharField(max_length=50)
    IBAN = serializers.CharField(max_length=50, read_only=True)
    bank_name = serializers.CharField(max_length=50, read_only=True)
    first_name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)
    image = serializers.CharField(max_length=100, read_only=True)

    def save(self, **kwargs):
        user = self.context['request'].user
        # raise CustomValidationError(_("Invalid OTP."))
        self.validated_data['IBAN'] = 'IBAN'
        self.validated_data['bank_name'] = 'bank_name'
        self.validated_data['first_name'] = 'first_name'
        self.validated_data['last_name'] = 'last_name'
        self.validated_data['image'] = '/profile/image/default.jpg'
        
        BankAccount.objects.create(
            user = user, 
            BIN = self.validated_data['BIN'], 
            IBAN = self.validated_data['IBAN'], 
            bank_name = self.validated_data['bank_name'], 
            image = self.validated_data['image'], 
        )
        return self.validated_data

class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'BIN', 'IBAN', 'bank_name', 'image']