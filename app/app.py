import datetime
import json
import os
import sqlite3
from typing import Union, Optional, Tuple, Literal
import investpy as ipy
import pathlib
import pandas
from .database import Database
from .transform import Transform
from .structures import Product, Etf, Stock, Config


Boolean = Literal[True, False]


class App:
    def __init__(self):
        self.today = datetime.date.today().strftime("%d/%m/%Y")
        self.config = self.load_config()
        self.db = Database()
        self.transforms = {"alphavantage": Transform.to_alphavantage}
        self.download_all()

    def download_all(self):
        products = Product.__subclasses__()
        for product in products:
            product_items = self.db.get_all_products(product)
            for item in product_items:
                print(f"Downloading data for {item.own_name}: ", end='')
                done = self.download(item)
                if done:
                    print("Success")
                else:
                    print("Failed")

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
    
    def download_data(self, product: Product, 
        dates: Optional[Tuple[str, str]] = None):
        if dates:
            from_date, to_date = dates
        else:
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

    def update_datafile(self, datafile: pandas.DataFrame, name: str):
        path = f"{self.config.output_folder}/{name}.csv"
        if pathlib.Path(path).is_file():
            datafile.to_csv(path, mode='a', header=False, index=False)
        else:
            self.save_datafile(datafile, name)

    def read_datafile(self, name: str)\
        -> Optional[pandas.DataFrame]:
        path = f"{self.config.output_folder}/{name}.csv"
        if pathlib.Path(path).is_file():
            return pandas.read_csv(path)

    def download(self, product: Product)\
        -> Boolean:
        data = self.download_data(product)
        of = self.config.output_format
        if of in self.transforms.keys():
            data = self.transforms[of](data)
        if isinstance(data, pandas.DataFrame):
            self.save_datafile(data, product.own_name)
            return True
        return False

    def update(self, product: Product):
        data = self.read_datafile(product.own_name)
        if isinstance(data, pandas.DataFrame):
            self.update_data(data, product)
        else:
            self.download(product)

    def update_data(self, data, product):
        def prep(date1, date2):
            return date1.strftime("%d/%m/%Y"),\
                date2.strftime("%d/%m/%Y")

        first_date = data.iloc[0:0]
        last_date = data.iloc[-1:0]
        first_date = datetime.datetime.strptime(
            first_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(
            last_date, "%Y-%m-%d")

        from_date = datetime.datetime.strptime(
            str(product.from_date), "%d/%m/%Y")
        to_date = datetime.datetime.strptime(
            str(product.to_date), "%d/%m/%Y")

        #case 5
        if any(from_date > last_date, to_date < first_date):
            self.download(product)
            return
        
        #case 2
        if all(first_date <= from_date <= last_date,
               first_date <= to_date <= last_date):
            return

        #case 1
        if from_date > first_date:
            from_date = last_date
            right_data = self.download_data(product, prep(from_date, to_date))
            self.update_datafile(right_data, product.own_name)
            return
        #cases 4 3
        else:
            #case 3
            if to_date <= last_date:
                to_date = first_date
                left_data = self.download_data(product, prep(from_date, to_date))
                data = left_data + data
                self.save_datafile(data, product.own_name)
            #case 4
            else:
                to_date_1 = first_date
                left_data = self.download_data(product, prep(from_date, to_date_1))
                from_date = last_date
                right_data = self.download_data(product, prep(from_date, to_date))
                data = left_data + data + right_data

        self.save_datafile(data, product.own_name)
