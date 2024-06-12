import json
from basic_info.models import Digitalcurrency

with open('basic_info/static_data/digital_currency.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for coin in data['coins']:
        obj, created = Digitalcurrency.objects.get_or_create(coin_id=coin['id'], coin_name=coin['name'],)