import requests
import json
from tkinter import *
from tkinter import messagebox as mb


def exchange_crypt():


ws = Tk()
ws.title('Курс обмена криптовалюты')
ws.geometry('360x180')

Label(text='Введите код криптовалюты: ').pack(padx=10, pady=10)

entry = Entry()
entry.pack(padx=10, pady=10)

Button(text='Получить курс обмена к рублю', command=exchange_crypt).pack(padx=10, pady=10)
ws.mainloop()
