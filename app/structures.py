from typing import NamedTuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    own_name: str
    name: str
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
    output_format: str = "investing"
    from_date: str = "01/01/2000"
    to_date: str = "today"
