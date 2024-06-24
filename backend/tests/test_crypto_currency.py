from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from basic_info.models import CryptoCurrency



class TestListCryptoCurrensySerializer(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.crypto = CryptoCurrency.objects.create(
            coin_id='bitcoin',
            coin_name='Bitcoin',
            coin_symbol='BTC',
            coin_image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTco24XpBFMbGIURB1nW8VG3PY-hMblZPCW-A&s', 
            is_active=True
        )
        self.list_url = reverse('list')  

    def test_list_cryptocurrency(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['coin_id'], 'bitcoin')
        self.assertEqual(response.data[0]['coin_name'], 'Bitcoin')
        self.assertEqual(response.data[0]['coin_symbol'], 'BTC')
        self.assertEqual(response.data[0]['coin_image'], 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTco24XpBFMbGIURB1nW8VG3PY-hMblZPCW-A&s')

    from unittest.mock import patch



class TestSwapCryptoCurrensySerializer(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.swap_url = reverse('swap')  

    @patch.object(CoinGeckoAPI, 'get_price', return_value={'bitcoin': {'usd': 30000}, 'ethereum': {'usd': 2000}})
    def test_swap_crypto_success(self, mock_get_price):
        data = {
            'coin1': 'bitcoin',
            'coin2': 'ethereum',
            'number_of_coin1': 1.0
        }
        response = self.client.post(self.swap_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['number_of_coin2'], 15.0)  # 30000 / 2000

    def test_swap_crypto_missing_fields(self):
        data = {
            'coin1': 'bitcoin',
            'number_of_coin1': 1.0
        }
        response = self.client.post(self.swap_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestSwapDollarCryptoCurrensySerializer(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.swap_dollar_url = reverse('swap-dollar-count')  

    @patch.object(CoinGeckoAPI, 'get_price', return_value={'bitcoin': {'usd': 30000}})
    def test_swap_dollar_to_crypto_success(self, mock_get_price):
        data = {
            'coin': 'bitcoin',
            'dollar': 30000
        }
        response = self.client.post(self.swap_dollar_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['number_of_coin'], 1.0)

    @patch.object(CoinGeckoAPI, 'get_price', return_value={'bitcoin': {'usd': 30000}})
    def test_swap_crypto_to_dollar_success(self, mock_get_price):
        data = {
            'coin': 'bitcoin',
            'number_of_coin': 1.0
        }
        response = self.client.post(self.swap_dollar_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dollar'], 30000)

    def test_swap_missing_fields(self):
        data = {
            'coin': 'bitcoin'
        }
        response = self.client.post(self.swap_dollar_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

