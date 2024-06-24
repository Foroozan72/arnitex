from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .serializers import WalletSerializer

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
