import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk


def update_cur_label(event):
    code = crypt_Combobox.get()
    name = currencies[code]
    cur_label.config(text=name)


def update_money_label(event):
    code = money_Combobox.get()
    name = currencies_money[code]
    money_label.config(text=name)


def exchange_crypt():
    code = crypt_Combobox.get().lower()
    if code:
        try:
            response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,tether,binancecoin,solana,ripple,cardano,avalanche,polkadot,dogecoin&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h&locale=en')
            response.raise_for_status()
            data = response.json()

            found = False
            for coin in data:
                if coin['symbol'].lower() == code:
                    exchange_symbol = coin['symbol'].upper()
                    exchange_price = coin['current_price']
                    date_update = coin['last_updated']
                    date_Label.config(text=date_update)
                    course_label.config(text=f'{exchange_price} $ за 1 {exchange_symbol}')
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
    'USDT': 'Tether',
    'BNB': 'Binance Coin',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'DOT': 'Polkadot',
    'DOGE': 'Dogecoin',
}

currencies_money={
    'RUB': 'Российский рубль',
    'CNY': 'Китайский юань',
    'USD': 'Американский доллар',
    'EUR': 'Европейский евро',
}

ws = Tk()
ws.title('Курс обмена криптовалюты')
ws.geometry('500x250')

f1 = Frame()
f2 = Frame()
f3 = Frame()
f4 = Frame()
f5 = Frame()
f6 = Frame()
f1.pack(pady=5)
f2.pack(pady=5)
f3.pack(pady=5)
f4.pack(pady=5)
f5.pack(pady=5, anchor='nw')
f6.pack(pady=5, anchor='nw')

Label(f1).pack()
Label(f2, text='Выберите криптовалюту: ', width=20, anchor="e").pack(side='left')

crypt_Combobox = ttk.Combobox(f2, values=list(currencies.keys()))
crypt_Combobox.pack(side='left')
crypt_Combobox.bind('<<ComboboxSelected>>', update_cur_label)

cur_label = ttk.Label(f2, width=21)
cur_label.pack(side='left', padx=10)



Label(f3, text='Выберите валюту: ', width=20, anchor="e").pack(side='left')

money_Combobox = ttk.Combobox(f3, values=list(currencies_money.keys()))
money_Combobox.pack(side='left')
money_Combobox.bind('<<ComboboxSelected>>', update_money_label)

money_label = ttk.Label(f3, width=21)
money_label.pack(side='left', padx=10)


Button(f4, text='Получить курс обмена', command=exchange_crypt).pack()

label = Label(f5, text='Дата последнего обновления курса: ', width=30).pack(side='left')
date_Label = ttk.Label(f5, font= 'Courier 14 bold')
date_Label.pack(side='left')

Label(f6, text='Курс обмена: ', width=20).pack(side='left', padx=35)
course_label = ttk.Label(f6, font= 'Courier 14 bold')
course_label.pack(side='left')


ws.mainloop()
