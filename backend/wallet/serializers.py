from rest_framework import serializers
from .models import Transaction, Wallet

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


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    Serializes the user_wallet, action, amount, and timestamp fields.

    Fields:
    - user_wallet: The wallet associated with the transaction.
    - action: The action of the transaction.
    - amount: The amount of the transaction.
    - timestamp: The timestamp of the transaction.
    """
    user_wallet = serializers.SlugRelatedField(slug_field='wallet_id', queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ['user_wallet', 'action', 'amount', 'timestamp']

    def create(self, validated_data):
        """
        Create and return a new `Transaction` instance, given the validated data.
        """
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Transaction` instance, given the validated data.
        """
        instance.user_wallet = validated_data.get('user_wallet', instance.user_wallet)
        instance.action = validated_data.get('action', instance.action)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.save()
        return instance


class TransferSerializer(serializers.Serializer):
    target_wallet_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)

    def validate(self, data):
        source_wallet = self.context['source_wallet']
        try:
            target_wallet = Wallet.objects.get(wallet_id=data['target_wallet_id'])
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Target wallet does not exist")

        if source_wallet.balance < data['amount']:
            raise serializers.ValidationError("Insufficient balance in the source wallet")

        if source_wallet == target_wallet:
            raise serializers.ValidationError("Cannot transfer to the same wallet")

        data['target_wallet'] = target_wallet
        return data
