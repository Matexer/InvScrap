import unittest
import random
import pandas
import pathlib
import os
from typing import Optional
from app import App
from app.structures import Product, Etf, Stock


DOWNLOAD_ALLOWED = False
TEST_DATA_FOLDER = "tests/test_data"


class TestApp(unittest.TestCase):
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        self.app = App(test=True)
        self.db = self.app.db

    def load_data(self, product: Product)\
        -> Optional[pandas.DataFrame]:
        path = f"{TEST_DATA_FOLDER}/{product.own_name}.csv"
        if pathlib.Path(path).is_file():
            return pandas.read_csv(path, index_col=False)
        elif DOWNLOAD_ALLOWED:
            path = f"{TEST_DATA_FOLDER}"
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
            with self.subTest(product=product):
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
                self.assertTrue(isinstance(data, pandas.DataFrame))
                self.app.save_datafile(data, item.own_name)
                r_data = self.app.read_datafile(item.own_name)
                self.assertTrue(data.equals(r_data))

