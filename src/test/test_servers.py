import unittest
import sys

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.resources.servers import ServersPing

class TestCase(unittest.TestCase):

    def test_post_action(sellf):
        service = ServersPing()
        expected = "POST request on /api/v1/servers/ping"
        assert service.post() == expected

if __name__ == '__main__':
    unittest.main()

