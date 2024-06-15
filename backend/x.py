from pycoingecko import CoinGeckoAPI
import datetime

# اتصال به API کوین‌گکو
cg = CoinGeckoAPI()

# دریافت اطلاعات 20 ارز دیجیتال برتر
top_coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=20, page=1)

# نمایش اطلاعات ارزها
for coin in top_coins:
    name = coin['name']
    logo = coin['image']
    current_price = coin['current_price']
    price_change_24h = coin['price_change_percentage_24h']

    # print(f"Name: {name}")
    # print(f"Logo URL: {logo}")
    # print(f"Current Price: ${current_price}")
    # print(f"24h Change: {price_change_24h:.2f}%")
    # print('-----------------------------')
    # print('-----------------------------')
    
    # # # نمایش لوگو
    # response = requests.get(logo)
    # img = Image.open(BytesIO(response.content))
    # img.show()

    # دریافت و نمایش نمودار هفتگی
    market_data = cg.get_coin_market_chart_by_id(id=coin['id'], vs_currency='usd', days=7)
    prices = market_data['prices']
    times = [datetime.datetime.fromtimestamp(price[0] / 1000) for price in prices]
    values = [price[1] for price in prices]
    print('----', times)

    # plt.figure(figsize=(10, 5))
    # plt.plot(times, values)
    # plt.title(f'{name} Weekly Price Chart')
    # plt.xlabel('Date')
    # plt.ylabel('Price (USD)')
    # plt.grid(True)
    # plt.show()
