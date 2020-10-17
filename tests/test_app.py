import unittest
from app import App


class TestApp(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = App()

