from rest_framework import serializers
from .models import Transaction, Wallet
from django.db import transaction
from django.utils import timezone
from utils.enums import TransactionActionChoices
from rest_framework import serializers


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


class TransferSerializer(serializers.Serializer):
    target_wallet_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)

    def validate(self, data):
        request = self.context['request']
        user = request.user
        print('user', user)
        
        try:
            source_wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Source wallet does not exist")

        try:
            target_wallet = Wallet.objects.get(wallet_id=data['target_wallet_id'])
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Target wallet does not exist")

        if source_wallet.balance < data['amount']:
            raise serializers.ValidationError("Insufficient balance in the source wallet")

        if source_wallet == target_wallet:
            raise serializers.ValidationError("Cannot transfer to the same wallet")

        data['source_wallet'] = source_wallet
        data['target_wallet'] = target_wallet
        return data

    def save(self, **kwargs):
        source_wallet = self.validated_data['source_wallet']
        target_wallet = self.validated_data['target_wallet']
        amount = self.validated_data['amount']

        with transaction.atomic():
            source_wallet.balance -= amount
            source_wallet.save()
            target_wallet.balance += amount
            target_wallet.save()

            Transaction.objects.create(
                user_wallet=source_wallet,
                action=TransactionActionChoices.INTERNAL_TRANSFER,
                amount=-amount,
                timestamp=timezone.now(),
                sender=source_wallet.user,
                receiver=target_wallet.user
            )

            Transaction.objects.create(
                user_wallet=target_wallet,
                action=TransactionActionChoices.INTERNAL_TRANSFER,
                amount=amount,
                timestamp=timezone.now(),
                sender=source_wallet.user,
                receiver=target_wallet.user
            )