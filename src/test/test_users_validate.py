import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.users import UsersValidate

path = "/api/v1/users/validate"

class TestCase(unittest.TestCase):

    def test_post_action(self):
        service = UsersValidate()
        expected = "POST request on " + path
        assert service.post() == expected

if __name__ == '__main__':
    unittest.main()
