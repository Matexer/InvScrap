import sqlite3
import os
from dataclasses import astuple
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

    def execute(self, order):
        self.connection.executescript(order)
        self.connection.commit()
    
    def is_name_free(self, name):
        tabs = tuple(tables.values())
        for tab in tabs:
            result = self.connection.executescript(
                f"SELECT EXISTS(SELECT 1 FROM {tab} WHERE" 
                f"'own_name'='%{name}%' LIMIT 1);")
            result = self.connection.cursor().fetchall()
            if result:
                return False
        return True
    
    def insert(self, product: Product, *, overwrite=False):
        table = tables[product.__class__]
        if not overwrite:
            self.execute(
                f"INSERT INTO {table} VALUES " +
                str(astuple(product)))
        else:
            self.execute(
                f"INSERT OR REPLACE INTO {table} VALUES " +
                str(astuple(product)))

    def delete(self, product: Product):
        table = tables[product.__class__]
        self.execute(f"DELETE FROM {table} "
                     f"WHERE own_name LIKE '%{product.own_name}%';")
