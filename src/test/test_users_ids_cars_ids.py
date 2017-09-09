import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.users import UsersIdsCarsIds

path = "/api/v1/users/"

class TestCase(unittest.TestCase):

    def test_get_action(self):
        service = UsersIdsCarsIds()
        expected = "GET request on " + path + "1/cars/1"
        assert service.get(1, 1) == expected

    def test_put_action(self):
        service = UsersIdsCarsIds()
        expected = "PUT request on " + path + "1/cars/1"
        assert service.put(1, 1) == expected
    
    def test_delete_action(self):
        service = UsersIdsCarsIds()
        expected = "DELETE request on " + path + "1/cars/1"
        assert service.delete(1, 1) == expected
   
if __name__ == '__main__':
    unittest.main()
