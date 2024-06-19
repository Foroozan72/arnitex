import requests

url = f"https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250, 
    'page': 1
}
response = requests.get(url, params=params)
x = []
for i in response.json():
    x.append({'id': i['id'], 'name': i['name']})

params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250, 
    'page': 2
}
response = requests.get(url, params=params)
for i in response.json():
    x.append({'id': i['id'], 'name': i['name']})

print('----------')
print('----------')
print('----------')
print(x)