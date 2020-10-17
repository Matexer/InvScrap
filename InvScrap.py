TEST = True

if not TEST:
    from app import App
    App()
else:
    import unittest
    from tests import TestDatabase
    unittest.main(verbosity=2)