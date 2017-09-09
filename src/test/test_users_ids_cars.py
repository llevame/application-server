import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.users import UsersIdsCars

path = "/api/v1/users/"

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = UsersIdsCars()
        expected = "GET request on " + path + "1/cars"
        assert service.get(1) == expected

    def test_post_action(self):
        service = UsersIdsCars()
        expected = "POST request on " + path + "1/cars"
        assert service.post(1) == expected
    
if __name__ == '__main__':
    unittest.main()
