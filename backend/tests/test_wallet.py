from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Wallet

class TestCheckWalletView(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(wallet_id='test_wallet_123')
        self.check_wallet_url = reverse('wallet:check_wallet', kwargs={'wallet_id': 'test_wallet_123'})

    def test_check_wallet_exists(self):
        """
        Ensure the API returns 200 OK if the wallet exists.
        """
        response = self.client.get(self.check_wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'wallet_id': 'test_wallet_123'})

    def test_check_wallet_does_not_exist(self):
        """
        Ensure the API returns 204 No Content if the wallet does not exist.
        """
        url = reverse('wallet:check_wallet', kwargs={'wallet_id': 'non_existent_wallet'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TransferTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.wallet1 = Wallet.objects.create(user=self.user1, balance=100.0)
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=50.0)
        self.transfer_url = reverse('wallet:read_wallet-transfer', kwargs={'pk': self.wallet1.pk})

    def test_transfer_balance(self):
        data = {
            'target_wallet_id': self.wallet2.wallet_id,
            'amount': 30.0
        }
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, 70.0)
        self.assertEqual(self.wallet2.balance, 80.0)
        transactions = Transaction.objects.filter(user_wallet__in=[self.wallet1, self.wallet2])
        self.assertEqual(transactions.count(), 2)
