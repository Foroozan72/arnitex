import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from pycoingecko import CoinGeckoAPI
from basic_info.models import CryptoCurrency
from asgiref.sync import sync_to_async

class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.limit = int(self.scope['url_route']['kwargs']['limit'])
        await self.accept()
        self.cg = CoinGeckoAPI()
        self.supported_coins = await sync_to_async(list)(CryptoCurrency.objects.filter(is_active=True))
        self.coin_ids = [coin.coin_id for coin in self.supported_coins]
        await self.send_crypto_data()

    async def disconnect(self, close_code):
        pass

    async def send_crypto_data(self):
        while True:
            data = await sync_to_async(self.cg.get_price)(
                ids=self.coin_ids, 
                vs_currencies='usd', 
                include_market_cap='true', 
                include_24hr_change='true', 
                include_24hr_vol='true'
            )

            coins = [
                {
                    "coin_id": coin.coin_id,
                    "name": coin.coin_name,
                    "symbol": coin.coin_symbol,
                    "logo": coin.coin_image,
                    "current_price": data[coin.coin_id]['usd'],
                    "change_24h": data[coin.coin_id].get('usd_24h_change', 0),
                    "volume_24h": data[coin.coin_id].get('usd_24h_vol', 0),
                    "market_cap": data[coin.coin_id].get('usd_market_cap', 0)
                }
                for coin in self.supported_coins if coin.coin_id in data
            ]
            coins.sort(key=lambda x: x['market_cap'], reverse=True)

            # Limit the results
            limited_coins = coins[:self.limit]

            await self.send(text_data=json.dumps(limited_coins))
            await asyncio.sleep(5)  # Update every 5 seconds
