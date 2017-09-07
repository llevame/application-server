import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.default import Default

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = Default()
        expected = "Default endpoint on /api/v1"
        assert service.get() == expected

if __name__ == '__main__':
    unittest.main()
