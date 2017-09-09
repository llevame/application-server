import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.trips import TripsIds

class TestCase(unittest.TestCase):

    def test_post_action(self):
        service = TripsIds()
        expected = "GET request on /api/v1/trips/1"
        assert service.get(1) == expected

if __name__ == '__main__':
    unittest.main()

