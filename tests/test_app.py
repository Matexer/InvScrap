import unittest
import random
import pandas
import pathlib
import os
import datetime
from typing import Optional, NamedTuple
from app import App
from app.structures import Product, Etf, Stock


DOWNLOAD_ALLOWED = False
TEST_DATA_FOLDER = "tests/test_data"


class TestConfig(NamedTuple):
    output_folder: str = "./tests/output"
    output_format: str = "alphavantage"
    from_date: str = "05/08/2020"
    to_date: str = "27/10/2020"


class TestApp(unittest.TestCase):
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        self.app = App()
        self.app.config = TestConfig()
        self.db = self.app.db

    def load_data(self, product: Product)\
        -> Optional[pandas.DataFrame]:
        path = f"{TEST_DATA_FOLDER}/{product.own_name}.csv"
        if pathlib.Path(path).is_file():
            data = pandas.read_csv(path, index_col=False)
            first_date = datetime.datetime.strptime(
                str(data.iloc[0,0]), "%Y-%m-%d")
            last_date = datetime.datetime.strptime(
                str(data.iloc[-1,0]), "%Y-%m-%d")

            from_date = product.from_date
            to_date = product.to_date

            if not from_date:
                from_date = self.app.config.from_date
            if not to_date:
                to_date = self.app.config.to_date

            from_date = datetime.datetime.strptime(
                self.app.valid_date(from_date), "%d/%m/%Y")
            to_date = datetime.datetime.strptime(
                self.app.valid_date(to_date), "%d/%m/%Y")
            
            if from_date < first_date:
                from_date = first_date
            if to_date > last_date:
                to_date = last_date
            
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = to_date.strftime("%Y-%m-%d")

            start = data.index[data["Date"] == from_date].tolist()[0]
            end = data.index[data["Date"] == to_date].tolist()[0] + 1

            data = data.iloc[start:end].reset_index()
            return data
            
        elif DOWNLOAD_ALLOWED:
            path = TEST_DATA_FOLDER
            if not pathlib.Path(path).is_dir():
                os.mkdir(path)

            data = self.app.download_data(product)
            if not data:
                return

            path = f"{TEST_DATA_FOLDER}/{product.own_name}.csv"
            data.to_csv(path, index=False)
            return data

    @unittest.skipIf(not DOWNLOAD_ALLOWED,
        "Download during test is not allowed")
    def test_1_download_data(self):
        products = Product.__subclasses__()
        for product in products:
            items = self.db.get_all_products(product)
            if items:
                self.app.download_data(
                    random.choice(items))

    def test_2_save_read_datafile(self):
        products = Product.__subclasses__()
        for product in products:
            product_items = self.db.get_all_products(product)
            for item in product_items:
                data = self.load_data(item)
                of = self.app.config.output_format
                if of in self.app.transforms.keys():
                    data = self.app.transforms[of](data)
                self.assertTrue(isinstance(data, pandas.DataFrame))
                self.app.save_datafile(data, item.own_name)
                r_data = self.app.read_datafile(item.own_name)
                pandas.testing.assert_frame_equal(
                    data, r_data, check_index_type=0)

    def test_3_case_5_left(self):
        products = Product.__subclasses__()
        for product in products:
            product_items = self.db.get_all_products(product)
            for item in product_items:
                data = self.load_data(item)