from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self, ):        
        self.app = Flask(__name__)
        self.api = Api(self.app,
            version='1.0',
            title='Exposição do modelo - MLE',
            description='API de Exposição do modelo - MLE',
            docs = '/docs'
        )        

    def run(self, ):
        self.app.run(
            host = '0.0.0.0',
            debug = True #Deve ser False, pois Por que fala no desafio que a aplicacao deve estar pronta pra producao
        )

server = Server()

