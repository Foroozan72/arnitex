from rest_framework import viewsets, mixins , status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Wallet ,Transaction
from .serializers import WalletSerializer , TransactionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import action


class CreateWalletViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to create a new Wallet object with a 15-digit wallet_id.
    
    Methods:
    - create(request, *args, **kwargs): Handles POST requests to create a wallet.
    
    Inputs:
    - request: The HTTP request containing user details in POST data.
    
    Outputs:
    - response: JSON response containing wallet details or error details on failure.
    
    Permissions:
    - IsAuthenticated: Requires user to be authenticated.
    """
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        wallet = Wallet(user=user)
        wallet.save()

        serializer = self.get_serializer(wallet)
        return Response(serializer.data)


class WalletReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for viewing Wallet objects.

    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all wallets.
    - retrieve(request, *args, **kwargs): Retrieves a wallet by its ID.

    Inputs:
    - request: The HTTP request containing necessary data for the respective actions.

    Outputs:
    - response: JSON response with the details of the wallet or a list of wallets.

    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['user']
    ordering_fields = ['wallet_id', 'user', 'balance']
    search_fields = ['wallet_id', 'user__username', 'balance']



class TransactionReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for viewing Transaction objects.
    
    Methods:
    - list(request, *args, **kwargs): Retrieves a list of all transactions.
    - retrieve(request, *args, **kwargs): Retrieves a transaction by its ID.
    
    Inputs:
    - request: The HTTP request containing necessary data for the respective actions.
    
    Outputs:
    - response: JSON response with the details of the transaction or a list of transactions.
    
    Permissions:
    - AllowAny: No authentication required.
    """
    permission_classes = [AllowAny]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # filterset_fields = ['user_wallet', 'action', 'timestamp']
    ordering_fields = ['timestamp', 'amount']
    search_fields = ['user_wallet__wallet_id', 'action']


class CheckWalletView(APIView):
    """
    View to check if a wallet ID exists.
    """
    def get(self, request, wallet_id):
        if Wallet.objects.filter(wallet_id=wallet_id).exists():
            return Response({'wallet_id': wallet_id}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class WalletViewSetTransfer(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Wallet model and
    includes a custom action to transfer balance between wallets.

    Permissions:
        - Requires the user to be authenticated to perform any actions.

    Actions:
        - list: Retrieve a list of all wallets.
        - create: Create a new wallet.
        - retrieve: Retrieve a specific wallet by ID.
        - update: Update a specific wallet.
        - partial_update: Partially update a specific wallet.
        - destroy: Delete a specific wallet.
        - transfer_balance: Transfer balance from one wallet to another.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='transfer')
    def transfer_balance(self, request, pk=None):
        source_wallet = self.get_object()
        serializer = TransferSerializer(data=request.data, context={'source_wallet': source_wallet})
        serializer.is_valid(raise_exception=True)
        target_wallet = serializer.validated_data['target_wallet']
        amount = serializer.validated_data['amount']

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

        return Response({'detail': 'Transfer successful'}, status=status.HTTP_200_OK)