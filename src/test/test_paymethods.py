import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.paymethods import Paymethods

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = Paymethods()
        expected = "GET request on /api/v1/paymethods"
        assert service.get() == expected

if __name__ == '__main__':
    unittest.main()
