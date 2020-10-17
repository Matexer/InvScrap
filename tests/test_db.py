import unittest
from typing import NamedTuple, Any
from app.database import Database
from app.structures import Stock, Etf


class TestDatabase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database(test=True)
        self.input_cases =\
            (Stock("Apple", "Apple Inc", "united states", 
                   "01/01/2018", "17/10/2020"),
            Etf("WIG 20 ETF", "Beta ETF WIG20TR Portfelowy FIZ",
                "poland", "01/01/2018", "17/10/2020", "Warsaw"))

    def test_1_insertion(self):
        for case in self.input_cases:
            self.db.insert(case)

    def test_2_is_name_free(self):
        f = self.db.is_name_free
        for case in self.input_cases:
            self.assertEqual(f((case.own_name)), False)

        for case in ("fasdjhf", "hfdsgfhf"):
            self.assertEqual(f((case)), True)

    def test_3_overwrite_insertion(self):
        for case in self.input_cases:
            self.db.insert(case, overwrite=True)

    def test_4_deletion(self):
        for case in self.input_cases:
            self.db.delete(case)
