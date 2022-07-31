import requests
import json
from config import keys


class ConvertionExseption(Exception):
    pass


class APIConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExseption(f'Невозможно перевести одинаковые валюты {quote}-{base}. Введите запрос еще раз.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {quote}. Введите запрос еще раз.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExseption(f'Не удалось обработать валюту {base}. Введите запрос еще раз.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExseption(f'Не удалось обработать количество {amount}. Введите запрос еще раз.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base *= float(amount)

        return total_base
