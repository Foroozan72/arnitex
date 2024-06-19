import json
import requests
from datetime import datetime
from support.models import Ticket
from basic_info.models import CryptoCurrency
from pycoingecko import CoinGeckoAPI

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

    def get_coin_data(coin_id):
        cg = CoinGeckoAPI()
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=7)
        market_data = cg.get_coins_markets(vs_currency='usd', ids=coin_id)
    
        coin_info = {
            "ID": market_data[0]['id'],
            "Name": market_data[0]['name'],
            "Symbol": market_data[0]['symbol'],
            "Current Price": market_data[0]['current_price'],
            "24h Change": market_data[0]['price_change_percentage_24h'],
            "24h Volume": market_data[0]['total_volume'],
            "Market Cap": market_data[0]['market_cap'],
            "Image": market_data[0]['image'],
            # "Weekly Chart": data['prices']
        }
        return coin_info

    def crypto_currencies(limit):
        valid_coins = APICryptoCurrency.local_coins()
        coins = []

        count = 0
        for i in valid_coins:
            if count == limit:
                break
            else:
                coins.append(APICryptoCurrency.get_coin_data(i))
                count+=1
        sorted_coin_list = sorted(coins, key=lambda x: x['Market Cap'], reverse=True)
        return sorted_coin_list
