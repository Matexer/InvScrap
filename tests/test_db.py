import unittest
from typing import NamedTuple, Any
from collections import defaultdict
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
            self.assertFalse(f(case.own_name))

        for case in ("fasdjhf", "hfdsgfhf"):
            self.assertTrue(f(case))

    def test_3_overwrite_insertion(self):
        for case in self.input_cases:
            self.db.insert(case, overwrite=True)

    def test_4_get_product(self):
        test_cases = ((p.__class__, p.own_name) 
                      for p in self.input_cases)
        f = self.db.get_product
        for case, result in zip(test_cases, self.input_cases):
            self.assertEqual(f(*case), result)

    def test_5_get_names(self):
        f = self.db.get_names
        names = defaultdict(list)
        for case in self.input_cases:
            names[case.__class__].append(case.own_name)
        
        for p_type, all_names in names.items():
            self.assertEqual(f(p_type), tuple(all_names))

    def test_6_deletion(self):
        for case in self.input_cases:
            self.db.delete(case)
