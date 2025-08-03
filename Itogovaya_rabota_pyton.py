import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image, ImageTk



currencies = {
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


currencies_money = {
    'RUB': 'Российский рубль',
    'CNY': 'Китайский юань',
    'USD': 'Американский доллар',
    'EUR': 'Европейский евро',
}


def update_cur_label(event): # Меняем метку с названием выбранной криптовалюты
    code = crypt_Combobox.get()
    name = currencies.get(code, "Неизвестная валюта")
    cur_label.config(text=name)


def update_money_label(event): # Меняем метку с названием выбранной валюты
    code = money_Combobox.get()
    name = currencies_money.get(code, "Неизвестная валюта")
    money_label.config(text=name)


def exchange_crypt():
    cr_code = crypt_Combobox.get().lower() # Получаем короткое обозначение криптовалюты
    mon_code = money_Combobox.get().lower() # Получаем короткое обозначение валюты

    if not cr_code or not mon_code: # Проверяем, выбрана ли валюта
        mb.showwarning('Внимание!', 'Выберите криптовалюту и валюту!')
        return

    try:
        # Запрос данных о криптовалютах по api-ссылке
        response = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=rub&ids=bitcoin,ethereum,tether,binancecoin,solana,ripple,cardano,avalanche,polkadot,dogecoin&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h&locale=en')
        response.raise_for_status()
        cr_data = response.json()

        # Запрос данных о валютах по api-ссылке
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        mon_data = response.json()
        mon_data = mon_data['Valute']

        # Находим информацию о криптовалюте
        found_crypto = False
        for cr_coin in cr_data:
            if cr_coin['symbol'].lower() == cr_code:
                exchange_symbol = cr_coin['symbol'].upper()
                exchange_price = cr_coin['current_price']
                date_update = cr_coin['last_updated'] # Находим дату последнего обновления курса
                date_update = date_update[0:10] + '  ' + date_update[11:19] # Редактируем строку с датой, отбрасывая лишнее
                date_Label.config(text=date_update) # Сообщаем дату последнего обновления курса

                # Проверяем выбран ли рубль, если выбран, то сразу сообщаем курс к рублю, так как по api сообщает курс к рублю
                found_currency = False
                if mon_code == 'rub':
                    exchange_price = round(exchange_price, 2)
                    course_label.config(text=f'{exchange_price:,}'.replace(',', ' ') + f' RUB за 1 {exchange_symbol}')
                    found_currency = True

                # Если выбран НЕ рубль, то обращаемся ко второй ссылке с курсом рубля к другим валютам
                else:
                    for mon_coin in mon_data.values():
                        if mon_coin['CharCode'].lower() == mon_code:
                            money_char = mon_coin['CharCode']
                            money_price = mon_coin['Value']  # Находим значение курса валюты к рублю
                            # Делим значение курса криптовалюты к рублю на курс рубля к валюте
                            exchange_price_rub = exchange_price / money_price
                            exchange_price_rub = round(exchange_price_rub, 2)
                            # Сообщаем курс криптовалюты к другой валюте
                            course_label.config(text=f'{exchange_price_rub:,}'.replace(',', ' ') + f' {money_char} за 1 {exchange_symbol}')
                            found_currency = True
                            break

                if not found_currency:
                    mb.showerror('Ошибка!', f'Валюта {mon_code.upper()} не найдена')

                found_crypto = True
                break

        if not found_crypto:
            mb.showerror('Ошибка!', f'Криптовалюта {cr_code.upper()} не найдена')

    except requests.exceptions.RequestException as e:
        mb.showerror('Ошибка сети', f'Не удалось получить данные: {e}')
    except Exception as e:
        mb.showerror('Ошибка', f'Произошла ошибка: {e}')


ws = Tk()
ws.title('Курс обмена криптовалюты')
w = ws.winfo_screenwidth()
h = ws.winfo_screenheight()
w2 = w//2 - 250
h2 = h//2 - 100
ws.geometry(f'500x250+{w2}+{h2}')


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

image_path = 'logo_itogo_small.jpg'
pil_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(pil_image)
label = Label(f1, image=tk_image)
label.pack() # Делаем красивый отступ сверу
Label(f2, text='Выберите криптовалюту: ', width=20, anchor="e").pack(side='left') # Заполняем первую строку окна через фрейм

crypt_Combobox = ttk.Combobox(f2, values=list(currencies.keys()))
crypt_Combobox.pack(side='left')
crypt_Combobox.bind('<<ComboboxSelected>>', update_cur_label)

cur_label = ttk.Label(f2, width=21)
cur_label.pack(side='left', padx=10)

Label(f3, text='Выберите валюту: ', width=20, anchor="e").pack(side='left') # Заполняем вторую строку окна через фрейм

money_Combobox = ttk.Combobox(f3, values=list(currencies_money.keys()))
money_Combobox.pack(side='left')
money_Combobox.bind('<<ComboboxSelected>>', update_money_label)

money_label = ttk.Label(f3, width=21)
money_label.pack(side='left', padx=10)

Button(f4, text='Получить курс обмена', command=exchange_crypt).pack() # Заполняем третью строку окна через фрейм

Label(f5, text='Дата последнего обновления курса: ', width=30, anchor="e").pack(side='left') # Заполняем четвёртую строку окна через фрейм
date_Label = ttk.Label(f5, font='Courier 14 bold') # В этой метке сообщаем дату последнего обновления курса криптовалюты
date_Label.pack(side='left')

Label(f6, text='Курс обмена: ', width=30, anchor="e").pack(side='left') # Заполняем пятую строку окна через фрейм
course_label = ttk.Label(f6, font='Courier 14 bold') # В этой метке сообщаем курс криптовалюты на указанную дату обновления
course_label.pack(side='left')

ws.mainloop()

