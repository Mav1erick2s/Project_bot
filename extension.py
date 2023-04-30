import json
import requests
from config import keys, TOKEN

class ConvertionException(Exception): #Класс для вывода системных ошибок
    pass

class APIExeption: #Класс для определения и вывода ошибок пользователя
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевест одинаковые валюты: "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except KeyError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = float(total_base)
        return total_base * amount #Возвращаем нужную сумму в валюте

