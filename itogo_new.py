import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk


currencies_money={
    'RUB': 'Российский рубль',
    'CNY': 'Китайский юань',
    'USD': 'Американский доллар',
    'EUR': 'Европейский евро',
}


def crypto_price():
    result = []
    try:
       for currency in currencies_money:
           currency == currency.lower()
           url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1&sparkline=false'
           response = requests.get(url)
           response.raise_for_status()
           data = response.json()
           for i, coin in enumerate(data):
               if currency == 'rub':
                   result.append({
                       'name': coin['name'],
                       'symbol': coin['symbol'],
                       'date': coin ['last_updated'],
                       'prices': {
                           'rub': coin['current_price'],
                           'cny': None,
                           'usd': None,
                           'eur': None
                       }
                   })
               else:
                   result[i]['prices'][currency] = coin['current_price']
       return result

    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка", f"Не удалось получить данные: {e}")
        return None

def save_to_json(data, filename='crypto_price.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    crypto_data = crypto_price()
    save_to_json(crypto_data)
    print("Данные успешно сохранены в crypto_prices.json")