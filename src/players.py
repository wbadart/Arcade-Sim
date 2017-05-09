#!/usr/bin/env python3

'''
players.py

Contains the protocols and factories for
peer-to-peer connections.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging

from twisted.internet.protocol import Protocol, ServerFactory, ClientFactory

class Player1Server(Protocol):

    def __init__(self):
        logging.debug('Constructing P1 Server')

    def connectionMade(self):
        logging.info('P1 made connection')

    def dataReceived(self, data):
        logging.info('P1 Server got data: %s', data)

class Player1ServerFactory(ServerFactory):

    def buildProtocol(self, addr):
        return Player1Server()


#===============================================

class Player2Client(Protocol):

    def __init__(self):
        logging.debug('Constructing P2 client')

    def conenctionMade(self):
        logging.info('P2 made connection')

    def dataReceived(self, data):
        logging.info('P2 Client got data: %s', data)

class Player2ClientFactory(ClientFactory):

    def buildProtocol(self, addr):
        return Player2Client()

