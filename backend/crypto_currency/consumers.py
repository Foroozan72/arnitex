
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
                    coin_data = await self.get_historical_data(coin.coin_id)
                    weekly_data[coin.coin_id] = coin_data

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
                    "weekly_data": weekly_data[coin.coin_id]  # داده‌های هفتگی
                }
                for coin in self.supported_coins if coin.coin_id in data
            ]
            coins.sort(key=lambda x: x['market_cap'], reverse=True)

            limited_coins = coins[:self.limit]

            for coin in limited_coins:
                print(f"Generating chart for {coin['name']}")  # Debug: Check which coin is being processed
                print(f"Weekly data: {coin['weekly_data']}")  # Debug: Check the weekly data

                image_data = self.generate_chart_image(coin['weekly_data'])
                coin['chart_image'] = image_data

            await self.send(text_data=json.dumps(limited_coins))
            await asyncio.sleep(5)

    async def get_historical_data(self, coin_id):
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=7)
        response = await sync_to_async(self.cmc.cryptocurrency_quotes_historical)(
            id=coin_id,
            convert='USD',
            time_start=start_date.isoformat(),
            time_end=end_date.isoformat()
        )

        # Debug: Print the response to see its structure
        print(response.data)

        # Check the response structure and extract data accordingly
        if 'quotes' in response.data:
            historical_data = response.data['quotes']
            return [(quote['timestamp'], quote['quote']['USD']['price']) for quote in historical_data]
        else:
            # Handle the case where the response does not contain the expected data
            return []


    def generate_chart_image(self, weekly_data):
        dates = [data[0] for data in weekly_data]
        prices = [data[1] for data in weekly_data]

        # استفاده از میانگین متحرک برای صاف کردن داده‌ها
        window_size = 3  # اندازه پنجره میانگین متحرک کوتاه‌تر
        prices_smooth = self.moving_average(prices, window_size)
        dates_smooth = dates[window_size - 1:]  # تنظیم تاریخ‌ها برای تطابق با میانگین متحرک

        # تعیین رنگ بر اساس تغییرات قیمت
        if prices_smooth[-1] >= prices_smooth[0]:
            line_color = 'green'  # رنگ سبز برای تغییرات مثبت
        else:
            line_color = 'red'  # رنگ قرمز برای تغییرات منفی

        fig, ax = plt.subplots()
        ax.plot(dates_smooth, prices_smooth, color=line_color, linewidth=1.5)  # استفاده از رنگ تعیین شده و ضخامت خط

        # تنظیم محدوده محور Y به صورت پویا
        price_range = max(prices_smooth) - min(prices_smooth)
        if price_range == 0:  # در صورتی که تغییرات قیمتی وجود نداشته باشد
            min_price, max_price = min(prices_smooth) * 0.99, max(prices_smooth) * 1.01
        else:
            min_price, max_price = min(prices_smooth) - price_range * 0.1, max(prices_smooth) + price_range * 0.1
        ax.set_ylim(min_price, max_price)

        ax.set_facecolor('white')  # تنظیم رنگ پس‌زمینه نمودار به سفید
        ax.axis('off')  # حذف محورها

        fig.set_size_inches(3, 1.5)  # تنظیم اندازه نمودار

        # Save plot to a bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
        buf.seek(0)
        
        # Convert bytes buffer to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return image_base64


    def moving_average(self, data, window_size):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')