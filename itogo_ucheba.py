import requests
import json
from tkinter import *
from tkinter import messagebox as mb



def exchange_crypt():
    code = entry.get()
    if code:
        try:
            #response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,ripple,cardano,solana,polkadot,dogecoin,chainlink&vs_currencies=usd,rub')
            response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,tether,binancecoin,solana,ripple,cardano,avalanche,polkadot,dogecoin&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h&locale=en')
            response.raise_for_status()
            data = response.json()
            if code in data['symbol']:
                exchange_symbol = data['symbol'](code)
                exchange_price = data['current_price'](code)
                mb.showinfo('Курс обмена', f'Курс: {exchange_price}$ за 1 {exchange_symbol}')
            else:
                mb.showerror('Ошибка!', f'Криптовалюта {code} не найдена')
        except Exception as e:
            mb.showerror('Ошибка', f'Произошла ошибка: {e}')
    else:
        mb.showwarning('Внимание!', 'Введите код криптовалюты!')



ws = Tk()
ws.title('Курс обмена криптовалюты')
ws.geometry('360x180')

Label(text='Введите код криптовалюты: ').pack(padx=10, pady=10)

entry = Entry()
entry.pack(padx=10, pady=10)

Button(text='Получить курс обмена к рублю', command=exchange_crypt).pack(padx=10, pady=10)
ws.mainloop()
