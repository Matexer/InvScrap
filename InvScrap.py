TEST = True

if TEST:
    import unittest
    from tests import TestDatabase
    unittest.main(verbosity=2)
else:
    from app import App
    App()
