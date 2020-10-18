from datetime import date
import json
import os
import sqlite3
from typing import Union, Optional
import investpy as ipy
import csv
import pathlib
import pandas
from .database import Database
from .structures import Product, Etf, Stock, Config, TestConfig


class App:
    def __init__(self, test=False):
        self.today = date.today().strftime("%d/%m/%Y")
        if test:
            self.config = TestConfig()
        else:
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
        from_date, to_date = self.get_dates(product)
        if isinstance(product, Etf):
            return ipy.etfs.get_etf_historical_data(
                product.name, product.country, from_date,
                to_date, stock_exchange=product.stock_exchange,
                as_json=False, order='ascending',
                interval='Daily')
        elif isinstance(product, Stock):
            return ipy.stocks.get_stock_historical_data(
                product.name, product.country, from_date,
                to_date, as_json=False, order='ascending',
                interval='Daily')

    def get_dates(self, product):
        from_date = product.from_date
        to_date = product.to_date
        if not from_date:
            from_date = self.config.from_date

        if not to_date:
            to_date = self.config.to_date

        from_date = self.valid_date(from_date)
        to_date = self.valid_date(to_date)
        return from_date, to_date

    def valid_date(self, date):
        if date == "today":
            return self.today
        return date

    def save_datafile(self, datafile: pandas.DataFrame, name: str):
        path = self.config.output_folder
        if not pathlib.Path(path).is_dir():
            os.mkdir(path)
        path = f"{self.config.output_folder}/{name}.csv"
        datafile.to_csv(path, index=False)

    def read_datafile(self, name: str)\
        -> Optional[pandas.DataFrame]:
        path = f"{self.config.output_folder}/{name}.csv"
        if pathlib.Path(path).is_file():
            return pandas.read_csv(path, index_col=False)