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

from twisted.internet.protocol import Protocol, Factory, ClientFactory

class Player1Server(Protocol):

    def __init__(self, gs):
        self.gs = gs
        logging.debug('Constructing P1 Server')

    def connectionMade(self):
        logging.info('P1 made connection')
        self.gs.multiplayer = True

    def dataReceived(self, data):
        logging.info('P1 Server got data: %s', data)
        self.gs.network_data.append(data)

class Player1ServerFactory(ClientFactory):

    def __init__(self, gs):
        self.gs         = gs
        self.connection = Player1Server(gs)

    def write(self, data):
        self.connection.transport.write(data)

    def buildProtocol(self, addr):
        return self.connection


#===============================================

class Player2Client(Protocol):

    def __init__(self, gs):
        self.gs = gs
        logging.debug('Constructing P2 client')
        self.connected = False

    def connectionMade(self):
        logging.info('P2 made connection')
        self.connected = True

    def dataReceived(self, data):
        logging.info('P2 Client got data: %s', data)
        self.gs.network_data.append(data)

class Player2ClientFactory(Factory):

    def __init__(self, gs):
        self.gs = gs
        self.connection = Player2Client(gs)

    def write(self, data):
        if self.connection.connected == True:
            self.connection.transport.write(data)

    def buildProtocol(self, addr):
        return self.connection

