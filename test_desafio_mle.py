# coding=utf-8
import unittest
from src.server.instance import server
from src.controllers.deck import *


class DesafioMLETests(unittest.TestCase):
    def test_getCard(self):
        self.assertEqual(Card.get(self, id=244), 
                         (200, '[{"id":244,"name":"Aetherfuel Alchemist","mana":6,"attack":4,"health":4,"type":"creature","god":"neutral","strategy":"late"}]')
                         )
if __name__ == "__name__":
    unittest.main()