import sqlite3
import os
from dataclasses import astuple
from typing import Tuple
from .structures import Product, Etf, Stock


tables = {Etf: "etfs",
          Stock: "stocks"}


class Database:
    def __init__(self, test=False):
        if test:
            db_name = "productsTestDB.db"
        else:
            db_name = "productsDB.db"

        if not os.path.isfile(db_name):
            self.connection = self.__create(db_name)
        else:
            self.connection = sqlite3.connect(db_name)

    @staticmethod
    def __create(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.executescript(
        f"""CREATE TABLE "{tables[Etf]}" (
        "own_name"	TEXT NOT NULL UNIQUE,
        "full_name"	TEXT NOT NULL UNIQUE,
        "country"	TEXT NOT NULL,
        "from_date"	TEXT NOT NULL,
        "to_date"	TEXT,
        "stock_exchange"	TEXT NOT NULL,
        PRIMARY KEY("own_name")
        );

        CREATE TABLE "{tables[Stock]}" (
        "own_name"	TEXT NOT NULL UNIQUE,
        "name"	TEXT NOT NULL UNIQUE,
        "country"	TEXT NOT NULL,
        "from_date"	TEXT NOT NULL,
        "to_date"	TEXT,
        PRIMARY KEY("own_name")
        );""")
        conn.commit()
        return conn

    def get_names(self, product: Product)\
        -> Tuple[str, ...]:
        table = tables[product]
        c = self.connection.cursor()
        c.execute(f"SELECT own_name FROM {table}")
        data = c.fetchall()
        return tuple(*data)

    def get_product(self, product: Product, name: str)\
        -> Product:
        table = tables[product]
        c = self.connection.cursor()
        c.execute(f"SELECT * FROM {table} WHERE own_name=? LIMIT 1", 
            (name, ))
        data = c.fetchone()
        return product(*data)

    def is_name_free(self, name: str)\
        -> True or False:
        c = self.connection.cursor()
        for tab in tables.values():
            c.execute(f"SELECT 1 FROM {tab} WHERE own_name=? LIMIT 1", 
                      (name, ))
            result = c.fetchone()
            if result:
                return False
        return True

    def insert(self, product: Product, *, overwrite=False):
        table = tables[product.__class__]
        c = self.connection.cursor()
        if not overwrite:
            c.execute(
                f"INSERT INTO {table} VALUES " +
                str(astuple(product)))
        else:
            c.execute(
                f"INSERT OR REPLACE INTO {table} VALUES " +
                str(astuple(product)))
        self.connection.commit()

    def delete(self, product: Product):
        table = tables[product.__class__]
        c = self.connection.cursor()
        c.execute(f"DELETE FROM {table} WHERE own_name LIKE ?;",
            (product.own_name, ))
        self.connection.commit()
