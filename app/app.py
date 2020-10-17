from datetime import date
import json
import os
import sqlite3
from typing import Union
import investpy as ipy
from .database import Database
from .structures import Product, Etf, Stock, Config


class App:
    def __init__(self):
        self.today = date.today().strftime("%d/%m/%Y")
        self.config = self.load_config()
        self.db = Database()

    @staticmethod
    def load_config() -> Config:
        if not os.path.isfile("./config.json"):
            with open('config.json', "w") as config_file:
                json.dump(Config()._asdict(), config_file,
                          indent=2, separators=(',', ': '))
            return Config()

        with open('config.json') as config_file:
            data = json.load(config_file)
        return Config(**data)
    
    def download_data(self, product: Product):
        if isinstance(product, Etf):
            return ipy.etfs.get_etf_historical_data(
                product.full_name, product.country, product.from_date,
                product.to_date, stock_exchange=product.stock_exchange,
                as_json=False, order='ascending',
                interval='Daily')
        elif isinstance(product, Stock):
            return ipy.stocks.get_stock_historical_data(
                product.full_name, product.country, product.from_date,
                product.to_date, as_json=False, order='ascending',
                interval='Daily')
