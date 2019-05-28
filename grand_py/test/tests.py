import unittest
from grand_py.bot import Bot

class MyFirstTests(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(Bot.hello_world(), 'hello world')


