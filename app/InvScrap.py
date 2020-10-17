import investpy as ipy
from typing import NamedTuple
import time

FROM_DATE = "01/01/2018"


class Product(NamedTuple):
    name: str
    country: str
    from_date: str = FROM_DATE


class Etf(Product):
    stock_exchange: str


class App:
    def __init__(self):
        self.today = time.

    @staticmethod
    def download_etf_data(etf):
        ipy.etfs.get_etf_historical_data(
            etf.name, etf.country, etf.from_date,
            to_date, stock_exchange=etf.stock_exchange=,
            as_json=False, order='ascending',
            interval='Daily')