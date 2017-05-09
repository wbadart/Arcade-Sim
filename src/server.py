#!/usr/bin/env python3

'''
server.py

Server to connect to Arcade Sim players.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging

from twisted.internet.protocol  import Protocol, ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer     import DeferredQueue

class ProtocolP1(Protocol):
    def __init__(self):
        self.friend     = ProtocolP2(self)
        self.data_queue = DeferredQueue()

    def connectionMade(self):
        logging.debug('P1 connection made')
        self.friend.start_forwarding()
        #self.send_to_friend('INFO:friend_connected')

    def dataReceived(self, data):
        logging.debug('P1 got data "%s"', data)
        self.friend.transport.write(data)
        #self.data_queue.put(data)

    def set_friend(self, conn):
        logging.info('Setting P1 friend: %s', conn)
        self.friend = conn

class ProtocolP1Factory(ServerFactory):
    def __init__(self):
        self.connection = ProtocolP1()

    def buildProtocol(self, addr):
        return self.connection

#=======================================

class ProtocolP2(Protocol):
    def __init__(self, friend):
        self.friend     = friend
        self.data_queue = DeferredQueue()

    def connectionMade(self):
        logging.debug('P2 connection made')


    def dataReceived(self, data):
        logging.debug('P2 got data "%s"', data)
        self.data_queue.put(data)

    def start_forwarding(self):
        self.data_queue.get().addCallback(self.send_to_friend)

    def send_to_friend(self, data):
        logging.debug('P2 sent "%s" to friend', data)
        self.friend.transport.write(data)
        self.data_queue.get().addCallback(self.send_to_friend)

class ProtocolP2Factory(ServerFactory):
    def __init__(self, friend):
        self.connection = ProtocolP2(friend)

    def buildProtocol(self, addr):
        return self.connection

#=======================================


def main( PORT_P1=40007, PORT_P2=40019 ):
    '''Main server execution; start listening for gamers.'''
    from twisted.internet import reactor

    logging.basicConfig( level=logging.DEBUG
                       , format='[%(module)s][%(levelname)s]:%(message)s' )

    logging.info
    endpoint_p1, endpoint_p2 =\
            TCP4ServerEndpoint(reactor, PORT_P1)\
          , TCP4ServerEndpoint(reactor, PORT_P2)

    fact_p1 = ProtocolP1Factory()
    fact_p2 = ProtocolP2Factory(fact_p1.connection)
    fact_p1.connection.set_friend(fact_p2.connection)
    endpoint_p1.listen(fact_p1)
    endpoint_p2.listen(fact_p2)
    reactor.run()

if __name__ == '__main__': main()

