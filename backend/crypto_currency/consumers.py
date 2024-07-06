
######################## Coin Gek Co ########################
# import json
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from pycoingecko import CoinGeckoAPI
# from basic_info.models import CryptoCurrency

# class CryptoConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.limit = int(self.scope['url_route']['kwargs']['limit'])
#         await self.accept()
#         self.cg = CoinGeckoAPI()
#         self.supported_coins = await sync_to_async(list)(CryptoCurrency.objects.filter(is_active=True))
#         self.coin_ids = [coin.coin_id for coin in self.supported_coins]
#         await self.send_crypto_data()

#     async def disconnect(self, close_code):
#         pass

#     async def send_crypto_data(self):
#         while True:
#             data = await sync_to_async(self.cg.get_price)(
#                 ids=self.coin_ids, 
#                 vs_currencies='usd', 
#                 include_market_cap='true', 
#                 include_24hr_change='true', 
#                 include_24hr_vol='true'
#             )

#             coins = [
#                 {
#                     "coin_id": coin.coin_id,
#                     "name": coin.coin_name,
#                     "symbol": coin.coin_symbol,
#                     "logo": coin.coin_image,
#                     "current_price": data[coin.coin_id]['usd'],
#                     "change_24h": data[coin.coin_id].get('usd_24h_change', 0),
#                     "volume_24h": data[coin.coin_id].get('usd_24h_vol', 0),
#                     "market_cap": data[coin.coin_id].get('usd_market_cap', 0),
#                     "weekly_data": await self.get_weekly_data(coin.coin_id)
#                 }
#                 for coin in self.supported_coins if coin.coin_id in data
#             ]
#             coins.sort(key=lambda x: x['market_cap'], reverse=True)

#             # Limit the results
#             limited_coins = coins[:self.limit]

#             await self.send(text_data=json.dumps(limited_coins))
#             await asyncio.sleep(5)  # Update every 5 seconds

#     async def get_weekly_data(self, coin_id):
#         # Get the last 7 days data
#         data = await sync_to_async(self.cg.get_coin_market_chart_by_id)(id=coin_id, vs_currency='usd', days=7)
#         return data['prices']









######################## Coin Market Cap ########################
import json
import asyncio
import matplotlib.pyplot as plt
from io import BytesIO
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from coinmarketcapapi import CoinMarketCapAPI
from basic_info.models import CryptoCurrency
from PIL import Image
import base64
import datetime
import os

class CryptoTableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.limit = int(self.scope['url_route']['kwargs']['limit'])
        await self.accept()
        CoinMarketCap_API_KEY = os.environ.get("CoinMarketCap_API_KEY")
        self.cmc = CoinMarketCapAPI(CoinMarketCap_API_KEY)
        self.supported_coins = await sync_to_async(list)(CryptoCurrency.objects.filter(is_active=True))
        self.coin_ids = [coin.coin_id for coin in self.supported_coins]
        await self.send_crypto_data()

    async def disconnect(self, close_code):
        pass

    async def send_crypto_data(self):
        while True:
            ids = ','.join(self.coin_ids)
            
            response = await sync_to_async(self.cmc.cryptocurrency_quotes_latest)(
                id=ids,
                convert='USD'
            )
            data = response.data

            weekly_data = {}
            for coin in self.supported_coins:
                if coin.coin_id in data:
                    coin_data = []
                    for i in range(7):
                        date = (datetime.datetime.utcnow() - datetime.timedelta(days=i)).isoformat()
                        price = data[coin.coin_id]['quote']['USD']['price']
                        coin_data.append((date, price))
                    weekly_data[coin.coin_id] = coin_data[::-1]

            coins = [
                {
                    "coin_id": coin.coin_id,
                    "name": coin.coin_name,
                    "symbol": coin.coin_symbol,
                    "logo": coin.coin_image,
                    "current_price": data[coin.coin_id]['quote']['USD']['price'],
                    "change_24h": data[coin.coin_id]['quote']['USD'].get('percent_change_24h', 0),
                    "volume_24h": data[coin.coin_id]['quote']['USD'].get('volume_24h', 0),
                    "market_cap": data[coin.coin_id]['quote']['USD'].get('market_cap', 0),
                    "weekly_data": weekly_data[coin.coin_id] 
                }
                for coin in self.supported_coins if coin.coin_id in data
            ]
            coins.sort(key=lambda x: x['market_cap'], reverse=True)

            limited_coins = coins[:self.limit]

            for coin in limited_coins:
                image_data = self.generate_chart_image(coin['weekly_data'])
                coin['chart_image'] = image_data

            await self.send(text_data=json.dumps(limited_coins))
            await asyncio.sleep(5) 

    def generate_chart_image(self, weekly_data):
        dates = [data[0] for data in weekly_data]
        prices = [data[1] for data in weekly_data]

        fig, ax = plt.subplots()
        ax.plot(dates, prices, color='#800080')
        ax.axis('off') 

        fig.set_size_inches(2, 1)

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return image_base64





####################### Coin Market Cap (ba nemodar) ########################
import json
import asyncio
import matplotlib.pyplot as plt
from io import BytesIO
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from coinmarketcapapi import CoinMarketCapAPI
from basic_info.models import CryptoCurrency
from PIL import Image
import base64
import datetime
import numpy as np
from utils.classes import get_tether_price
from datetime import datetime

class CryptoTableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.limit = int(self.scope['url_route']['kwargs']['limit'])
        await self.accept()
        CoinMarketCap_API_KEY = os.environ.get("CoinMarketCap_API_KEY")
        self.cmc = CoinMarketCapAPI(CoinMarketCap_API_KEY)
        self.supported_coins = await sync_to_async(list)(CryptoCurrency.objects.filter(is_active=True))
        self.coin_ids = [coin.coin_id for coin in self.supported_coins]
        await self.send_crypto_data()

    async def disconnect(self, close_code):
        pass

    async def send_crypto_data(self):
        while True:
            ids = ','.join(self.coin_ids)
            
            response = await sync_to_async(self.cmc.cryptocurrency_quotes_latest)(
                id=ids,
                convert='USD'
            )
            data = response.data
            tether_price = get_tether_price()

            coins = [
                {
                    "coin_id": coin.coin_id,
                    "name": coin.coin_name,
                    "symbol": coin.coin_symbol,
                    "logo": coin.coin_image,
                    "current_price": data[coin.coin_id]['quote']['USD']['price'],
                    "sell_toman_price" : data[coin.coin_id]['quote']['USD']['price'] * tether_price['sell'],
                    "buy_toman_price" : data[coin.coin_id]['quote']['USD']['price'] * tether_price['buy'],
                    "change_24h": data[coin.coin_id]['quote']['USD'].get('percent_change_24h', 0),
                    "volume_24h": data[coin.coin_id]['quote']['USD'].get('volume_24h', 0),
                    "market_cap": data[coin.coin_id]['quote']['USD'].get('market_cap', 0)
                }
                for coin in self.supported_coins if coin.coin_id in data
            ]
            coins.sort(key=lambda x: x['market_cap'], reverse=True)

            limited_coins = coins[:self.limit]

            await self.send(text_data=json.dumps(limited_coins))
            print('--', datetime.now())
            await asyncio.sleep(4)
