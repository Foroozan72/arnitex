# import json
# from basic_info.models import CryptoCurrency

# with open('basic_info/static_data/crypto_currency.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     for coin in data['coins']:
#         obj, created = CryptoCurrency.objects.get_or_create(coin_id=coin['id'], coin_name=coin['name'],)

import requests
from basic_info.models import CryptoCurrency

url = f"https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250, 
    'page': 1
}
response = requests.get(url, params=params)
for i in response.json():
    obj, created = CryptoCurrency.objects.get_or_create(coin_id=i['id'], coin_name=i['name'], coin_symbol=i['symbol'].upper(), coin_image=i['image'])

params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250, 
    'page': 2
}
response = requests.get(url, params=params)
for i in response.json():
    obj, created = CryptoCurrency.objects.get_or_create(coin_id=i['id'], coin_name=i['name'], coin_symbol=i['symbol'].upper(), coin_image=i['image'])
