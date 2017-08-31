import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src import appServer

class TestCase(unittest.TestCase):

    def test_endPoint_api(self):
       appSer = appServer.ApplicationServer()
       expected = "Application Server api"
       assert appSer.get() == expected

    def test_endPoint_hp(self):
        homePage = appServer.HomePage()
        expected = "Homepage"
        assert homePage.get() == expected

if __name__ == '__main__':
    unittest.main()
