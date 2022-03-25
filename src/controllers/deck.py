from flask import Flask
from flask_restx import Resource, Api

from src.server.instance import server

from src.controllers.train import Train

app, api = server.app, server.api

#deck_db = [
#    {'id': -1, 'name': 'card test -1', 'mana': -1, 'attack': -1, 'health': -1, 'type': 'spell', 'god':'death', 'strategy': 'early'},
#    {'id':  0, 'name': 'card test 0', 'mana': -1, 'attack': -1, 'health': -1, 'type': 'spell', 'god':'death', 'strategy': 'early'},
#    {'id':  1, 'name': 'card test 1', 'mana': -1, 'attack': -1, 'health': -1, 'type': 'creature', 'god':'neutral', 'strategy': 'late'}
#]


@api.route('/getDeckList')
class DeckList(Resource):    
    def get(self, ):
        train = Train('challenge_train.csv','challenge_test.csv', 'challenge_result.csv')        
        if not train.arqResultExiste:            
            train.fit()
        return (200, train.getDeckComplete())



@api.route('/getCardById/<id>')
class Card(Resource):
    def get(self, id):        
        train = Train('challenge_train.csv','challenge_test.csv', 'challenge_result.csv')
        if not train.arqResultExiste:            
            train.fit()
        
        return (200, train.findCardById(int(id)))
        #return ([x for x in deck_db if x['id'] == id][0],None)
        