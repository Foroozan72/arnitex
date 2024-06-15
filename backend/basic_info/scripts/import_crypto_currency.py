import json
from basic_info.models import CryptoCurrency

with open('basic_info/static_data/crypto_currency.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for coin in data['coins']:
        obj, created = CryptoCurrency.objects.get_or_create(coin_id=coin['id'], coin_name=coin['name'],)