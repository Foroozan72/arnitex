import json
import requests
from datetime import datetime
from support.models import Ticket
from basic_info.models import CryptoCurrency

class GenerateTrackingCode():
    def dictionary(model):
        model_dict = {Ticket: "T"}
        return model_dict[model]

    def generate_tracking_code(model):
        today = datetime.now().strftime("%Y%m%d")
        today_objects_count = model.objects.filter(
            created_at__year=datetime.now().year,
            created_at__month=datetime.now().month,
            created_at__day=datetime.now().day
        ).count() + 1
        return f"{GenerateTrackingCode.dictionary(model)}{today}{today_objects_count:04d}"

class APICryptoCurrency():
    def local_coins():
        coins_id_list = []
        for i in CryptoCurrency.objects.filter(is_active=True):
            coins_id_list.append(i.coin_id)
        return coins_id_list

    def get_coins_info():
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'sparkline': 'true'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def crypto_currencies(limit):
        valid_coins = APICryptoCurrency.local_coins()
        all_coins = APICryptoCurrency.get_coins_info()
        coins = []

        count = 0
        for i in all_coins:
            if count == limit:
                break
            elif i['id'] in valid_coins:
                coins.append(i)
                count+=1
        return coins
