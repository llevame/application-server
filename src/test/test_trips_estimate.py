import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.trips import TripsEstimate

class TestCase(unittest.TestCase):

    def test_post_action(self):
        service = TripsEstimate()
        expected = "POST request on /api/v1/trips/estimate"
        service.post() == expected

if __name__ == '__main__':
    unittest.main()

