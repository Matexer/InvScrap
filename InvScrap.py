TEST = False

if TEST:
    import unittest
    from tests import TestDatabase
    from tests import TestApp
    unittest.main(verbosity=2)
else:
    from app import App
    App()