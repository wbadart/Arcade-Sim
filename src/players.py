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

class GameServerProtocol(Protocol):

    def __init__(self, gs):
        self.gs = gs

    def dataReceived(self, data):
        self.gs.push_network_data(data)

    def connectionMade(self):
        self.gs.multiplayer = True
        logging.warning('Player 2 connected')

class GameServerFactory(ServerFactory):

    def __init__(self, gs):
        self.connection = GameServerProtocol(gs)

    def buildProtocol(self, addr):
        return self.connection


class GameClientProtocol(Protocol):

    def __init__(self, gs):
        self.gs = gs

    def dataReceived(self, data):
        self.gs.push_network_data(data)

    def connectionMade(self):
        logging.warning('Connected to player 1')

class GameClientFactory(ClientFactory):

    def __init__(self, gs):
        self.connection = GameClientProtocol(gs)

    def buildProtocol(self, addr):
        return self.connection

