import requests
from basic_info.models import CryptoCurrency
import os

CryptoCurrency.objects.all().delete()
def get_top_500_cryptocurrencies(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '20',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    crypto_list = []
    for currency in data['data']:
        CryptoCurrency.objects.get_or_create(
            coin_id=currency['id'],
            coin_name=currency['name'],
            coin_symbol=currency['symbol'],
            coin_image=f"https://s2.coinmarketcap.com/static/img/coins/64x64/{currency['id']}.png"
        )

    return crypto_list

api_key = os.environ.get("CoinMarketCap_API_KEY")
crypto_data = get_top_500_cryptocurrencies(api_key)
