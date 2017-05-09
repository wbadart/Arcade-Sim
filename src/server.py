#!/usr/bin/env python3

'''
server.py

Server to connect to Arcade Sim players.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

from twisted.internet.protocol  import Protocol, ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer     import DeferredQueue

class ProtocolP1(Protocol):
    def __init__(self):
        self.friend     = None
        self.data_queue = DeferredQueue()

    def connectionMade(self):
        print('PLAYER ONE CONNETCION MADE')
        self.friend.start_forwarding()

    def dataReceived(self, data):
        self.data_queue.put(data)

    def start_forwarding(self):
        self.data_queue.get().addCallback(self.send_to_friend)

    def send_to_friend(self, data):
        self.friend.transport.write(data)

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
        print('PLAYER TWO CONNETCION MADE')
        self.friend.start_forwarding()

    def dataReceived(self, data):
        self.data_queue.put(data)

    def start_forwarding(self):
        self.data_queue.get().addCallback(self.send_to_friend)

    def send_to_friend(self, data):
        self.friend.transport.write(data)
        self.data_queue.get()

class ProtocolP2Factory(ServerFactory):
    def __init__(self, friend):
        self.connection = ProtocolP2(friend)

    def buildProtocol(self, addr):
        return self.connection

#=======================================


def main( PORT_P1=40007, PORT_P2=40008 ):
    '''Main server execution; start listening for gamers.'''
    from twisted.internet import reactor

    endpoint_p1, endpoint_p2 =\
            TCP4ServerEndpoint(reactor, PORT_P1)\
          , TCP4ServerEndpoint(reactor, PORT_P2)

    fact_p1 = ProtocolP1Factory()
    fact_p2 = ProtocolP2Factory(fact_p1.connection)
    fact_p1.connection.friend = fact_p2.connection
    endpoint_p1.listen(fact_p1)
    endpoint_p2.listen(fact_p2)
    reactor.run()

if __name__ == '__main__': main()

