from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Wallet ,Transaction
from .serializers import WalletSerializer , TransactionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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