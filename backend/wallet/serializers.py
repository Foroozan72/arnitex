from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.

    Serializes the wallet_id, user, and balance fields.

    Methods:
    - create: Creates a new Wallet instance.
    - update: Updates an existing Wallet instance.
    
    Fields:
    - wallet_id: The 15-digit unique identifier for the wallet.
    - user: The user to whom the wallet belongs.
    - balance: The balance amount in the wallet.
    """
    wallet_id = serializers.CharField(read_only=True)
    balance = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)

    class Meta:
        model = Wallet
        fields = ['wallet_id', 'user', 'balance']

    def create(self, validated_data):
        """
        Create and return a new `Wallet` instance, given the validated data.
        """
        user = validated_data.get('user')
        wallet = Wallet.objects.create(user=user)
        return wallet
