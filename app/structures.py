from typing import NamedTuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    own_name: str
    full_name: str
    country: str
    from_date: str
    to_date: str


@dataclass(frozen=True)
class Stock(Product):
    ...


@dataclass(frozen=True)
class Etf(Product):
    stock_exchange: str


class Config(NamedTuple):
    output_folder: str = "./output"
    from_date: str = "01/01/2018"
    to_date: str = "today"
