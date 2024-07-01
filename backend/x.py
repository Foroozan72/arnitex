import requests

def get_top_500_cryptocurrencies(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '500',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    crypto_list = []
    for currency in data['data']:
        crypto_list.append({
            'id': currency['id'],
            'name': currency['name'],
            'symbol': currency['symbol'],
            'logo': f"https://s2.coinmarketcap.com/static/img/coins/64x64/{currency['id']}.png"
        })

    return crypto_list

# جایگزین کردن API Key خودتان در اینجا
api_key = '6c5933f7-aa3f-4765-a83f-6797e6a298e5'
crypto_data = get_top_500_cryptocurrencies(api_key)

print("اطلاعات 500 ارز دیجیتال اول با موفقیت ذخیره شد.")
