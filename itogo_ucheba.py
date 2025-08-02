import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk

from bottle import response


def update_cur_labelk(event):
    code = Combobox.get()
    name = currencies[code]
    cur_label.config(text=name)

def exchange_crypt():
    code = Combobox.get().strip().lower()
    if code:
        try:
            #response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,ripple,cardano,solana,polkadot,dogecoin,chainlink&vs_currencies=usd,rub')
            #response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,tether,binancecoin,solana,ripple,cardano,avalanche,polkadot,dogecoin&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h&locale=en')
            response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=rub&order=market_cap_desc&per_page=10&page=1&sparkline=false')
            response.raise_for_status()
            data = response.json()

            found = False
            for coin in data:
                if coin['symbol'].lower() == code:
                    exchange_symbol = coin['symbol'].upper()
                    exchange_price = coin['current_price']
                    mb.showinfo('Курс обмена', f'Курс: {exchange_price} $ за 1 {exchange_symbol}')
                    found = True
                    break
            if not found:
                mb.showerror('Ошибка!', f'Криптовалюта {code.upper()} не найдена')
        except Exception as e:
            mb.showerror('Ошибка', f'Произошла ошибка: {e}')
    else:
        mb.showwarning('Внимание!', 'Введите код криптовалюты!')


currencies={
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'XRP': 'Ripple',
    'USDT': 'Tether',
    'BNB': 'Binancecoin',
    'SOL': 'Solana',
    'USDC': 'USD-coin',
    'STETH': 'Lido Staked Ether',
    'TRX': 'TRON',
    'DOGE': 'Dogecoin',
}

ws = Tk()
ws.title('Курс обмена криптовалюты')
ws.geometry('360x180')

Label(text='Выберите код криптовалюты: ').pack(padx=10, pady=10)

Combobox = ttk.Combobox(values=list(currencies.keys()))
Combobox.pack(padx=10, pady=10)
Combobox.bind('<<ComboboxSelected>>', update_cur_labelk)

cur_label = ttk.Label()
cur_label.pack(padx=10, pady=10)

Button(text='Получить курс обмена к доллару', command=exchange_crypt).pack(padx=10, pady=10)
ws.mainloop()
