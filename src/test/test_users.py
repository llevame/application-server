import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.users import Users

path = "/api/v1/users"

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = Users()
        expected = "GET request on " + path
        assert service.get() == expected

    def test_post_action(self):
        service = Users()
        expected = "POST request on " + path
        assert service.post() == expected

if __name__ == '__main__':
    unittest.main()
