import sqlite3
from dataclasses import astuple
from typing import Tuple, Type, Union, Literal
import pathlib
from .structures import Product, Etf, Stock


tables = {Etf: "etfs",
          Stock: "stocks"}

Boolean = Literal[True, False]


class Database:
    def __init__(self, test=False):
        if test:
            db_name = "productsTestDB.db"
        else:
            db_name = "productsDB.db"

        if pathlib.Path(db_name).is_file():
            self.connection = sqlite3.connect(db_name)
        else:
            self.connection = self.__create(db_name)


    @staticmethod
    def __create(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.executescript(
        f"""CREATE TABLE "{tables[Etf]}" (
        "own_name"	TEXT NOT NULL UNIQUE,
        "name"	TEXT NOT NULL UNIQUE,
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

    def get_names(self, product_type: Type[Product])\
        -> Tuple[str, ...]:
        table = tables[product_type]
        c = self.connection.cursor()
        c.execute(f"SELECT own_name FROM {table}")
        data = c.fetchall()
        return tuple(*data)

    def get_product(self, product_type: Type[Product], name: str)\
        -> Product:
        table = tables[product_type]
        c = self.connection.cursor()
        c.execute(f"SELECT * FROM {table} WHERE own_name=? LIMIT 1", 
            (name, ))
        data = c.fetchone()
        return product_type(*data)

    def get_all_products(self, product_type: Type[Product])\
        -> Tuple[Product, ...]:
        table = tables[product_type]
        c = self.connection.cursor()
        c.execute(f"SELECT * FROM {table}")
        data = c.fetchall()
        return tuple(product_type(*p_data) for p_data in data)

    def is_name_free(self, name: str)\
        -> Boolean:
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
        data = astuple(product)
        if len(data) > 1:
            part_2 = ", ?" * (len(data) - 1)
            part_2 = f"(?{part_2})"
        else:
            part_2 = "?"

        if not overwrite:
            part_1 = f"INSERT INTO {table} VALUES "
            order = part_1 + part_2
            c.execute(order, data)
        else:
            part_1 = f"INSERT OR REPLACE INTO {table} VALUES "
            order = part_1 + part_2
            c.execute(order, data)

        self.connection.commit()

    def delete(self, product: Product):
        table = tables[product.__class__]
        c = self.connection.cursor()
        c.execute(f"DELETE FROM {table} WHERE own_name LIKE ?;",
            (product.own_name, ))
        self.connection.commit()
