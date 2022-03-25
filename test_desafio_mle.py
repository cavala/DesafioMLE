# coding=utf-8
import unittest
from src.server.instance import server
from src.controllers.deck import *


class DesafioMLETests(unittest.TestCase):
    URL = 'http://localhost:5000/getDeckList/ '

    def setUp(self):
        self.resposta = requests.get(self.URL)
            
    def buscar_dados(self):
        self.assertEqual(200, self.resposta)

    def __init__():
        self.buscar_dados(self)
        print (self.assertEqual(200, self.resposta))