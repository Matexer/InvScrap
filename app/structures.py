from typing import NamedTuple, Tuple


class Product(NamedTuple):
    id_num: int
    own_name: str
    full_name: str
    country: str
    from_date: str
    to_date: str


class Stock(Product):
    eff: str


class Etf(Product):
    stock_exchange: str


class Config(NamedTuple):
    output_folder: str = "./output"
    from_date: str = "01/01/2018"
    to_date: str = "today"
