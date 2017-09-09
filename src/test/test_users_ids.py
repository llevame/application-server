import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.users import UsersIds

path = "/api/v1/users/"

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = UsersIds()
        expected = "GET request on " + path + "1"
        assert service.get(1) == expected

    def test_put_action(self):
        service = UsersIds()
        expected = "PUT request on " + path + "1"
        assert service.put(1) == expected
    
    def test_delete_action(self):
        service = UsersIds()
        expected = "DELETE request on " + path + "1"
        assert service.delete(1) == expected

if __name__ == '__main__':
    unittest.main()
