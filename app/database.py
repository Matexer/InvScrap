import sqlite3
import os
from typing import Union
from .structures import Product, Etf, Stock


etfs = "etfs"
stocks = "stocks"


class Database:
    def __init__(self):
        if not os.path.isfile("productsDB.db"):
            self.connection = self.__create()
        else:
            self.connection = sqlite3.connect("productsDB.db")

    @staticmethod
    def __create():
        conn = sqlite3.connect("productsDB.db")
        c = conn.cursor()
        c.executescript(
        f"""CREATE TABLE "{etfs}" (
        "own_name"	TEXT NOT NULL UNIQUE,
        "full_name"	TEXT NOT NULL UNIQUE,
        "country"	TEXT NOT NULL,
        "from_date"	TEXT NOT NULL,
        "to_date"	TEXT,
        "stock_exchange"	TEXT NOT NULL,
        PRIMARY KEY("own_name")
        );

        CREATE TABLE "{stocks}" (
        "own_name"	TEXT NOT NULL UNIQUE,
        "name"	TEXT NOT NULL UNIQUE,
        "country"	TEXT NOT NULL,
        "from_date"	TEXT NOT NULL,
        "to_date"	TEXT,
        PRIMARY KEY("own_name")
        );""")
        conn.commit()
        return conn
    
    def insert(self, product: Product):
        if isinstance(product, Etf):
            table = etfs
        elif isinstance(product, Stock):
            table = stocks
        self.connection.execute(
            f"INSERT INTO {table} VALUES " + str(tuple(product)))