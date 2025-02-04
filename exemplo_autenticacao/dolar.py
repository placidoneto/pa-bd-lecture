import requests
import json

# URL da API de dMoedas
url = "https://openexchangerates.org/api/v2.5,usd,bRL.json"

try:
    response = requests.get(url)
    data = response.json()
    
    # Obter o valor actual do dólar em BRL
    exchange_rate = data['data']['usd']['rate']
    print(f'O dólar (USD) está valendo R$ {round(exchange_rate, 4)} em hoje.')
except requests.exceptions.RequestException as e:
    print(f"Erro ao obter os dados: {e}")