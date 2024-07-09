import os
import requests
from datetime import datetime
from coinmarketcapapi import CoinMarketCapAPI
from support.models import Ticket

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


def get_tether_price():
    url = "https://api.nobitex.ir/market/stats"
    payload = {
        "srcCurrency": "usdt",
        "dstCurrency": "rls"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return {'buy': int(data['stats']['usdt-rls']['bestBuy']), 'sell': int(data['stats']['usdt-rls']['bestSell'])}



def crypto_currency_inf(id):
    CoinMarketCap_API_KEY = os.environ.get("CoinMarketCap_API_KEY")
    cmc = CoinMarketCapAPI(CoinMarketCap_API_KEY)

    
    response = cmc.cryptocurrency_quotes_latest(
        id=id,
        convert='USD'
    )
    data = response.data
    return data