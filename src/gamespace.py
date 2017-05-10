#!/usr/bin/env python3

'''
gamespace.py

Over-arching class to wrap pygame functionality.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging
import pygame
import sys

from twisted.internet.task     import LoopingCall
from twisted.internet.protocol import Protocol, Factory
from twisted.internet          import reactor

from src.gameobj import GameObj, Menu, Button
from src.loader  import ModuleLoader
from src.players import GameClientFactory, GameServerFactory

class GameSpace(object):

    def __init__(self, player, config={}):

        # Initialize library and intstnace properties
        pygame.init()
        self.config      = config
        self.multiplayer = False if player == 1 else True

        # Configure pygame window
        self.size   = self.width, self.height = config.get('width'), config.get('height')
        self.screen = pygame.display.set_mode(self.size)
        self.clock  = pygame.time.Clock()
        self.tick   = config.get('tick') or 30

        # Configure keymapping; this establishes a mapping from the "command" (up/
        # down/etc, keys of the config keymap) to the corresponding pygame key const
        # Ultimately maps ascii_code -> command
        self.keymap  = { ord(self.config['keymap'][c]): c for c in self.config['keymap'] }

        # Set up the module loader
        loader      = ModuleLoader('./config.yml')
        self.module = sys.modules[__name__]

        # Set up the main menu w/ background stuff
        screen_bg = pygame.Surface((self.width, self.width))
        screen_bg.fill((0, 0, 0))
        screen_bg = screen_bg, screen_bg.get_rect()

        control_bg = pygame.Surface((self.width, self.height - self.width))
        control_bg.fill((45, 45, 45))
        control_bg = control_bg, (0, self.width)

        help_label = pygame.font.SysFont('Helvetica', 16)\
                           .render('Press "h" for help and "m" for menu.', 10, (165, 165, 165))
        help_label = help_label, ( self.width / 2 - help_label.get_width() / 2
                                 , self.height - help_label.get_height() )

        self.backgrounds = [ screen_bg, control_bg, help_label ]
        menu_img         =   pygame.image.load('./assets/menu_bg.jpg')
        menu_img         =   pygame.transform.scale(menu_img, (self.width, self.width))
        self.menu_img    =   menu_img, menu_img.get_rect()

        # Set up control visuals
        self.controls = pygame.sprite.RenderPlain(
                [ GameObj({ 'default': './assets/stick-center.png'
                          , 'up':      './assets/stick-up.png'
                          , 'left':    './assets/stick-left.png'
                          , 'down':    './assets/stick-down.png'
                          , 'right':   './assets/stick-right.png'
                          }, 10, self.width + 20, self.keymap )
                , GameObj({ 'default': './assets/button_a_up.png'
                          , 'A':       './assets/button_a_down2.png'
                          }, self.width / 2 + 20, self.width + 20, self.keymap )

                , GameObj({ 'default': './assets/button_b_up.png'
                          , 'B':       './assets/button_b_down.png'
                          }, self.width / 2 + 168, self.width + 20, self.keymap ) ])

        self.menu = Menu([ Button(m.name, m, not i) for i, m in enumerate(loader.modules) ]
                         , self, self.width / 2 - Button.width / 2, 10, self.keymap )

        # Configure multiplayer
        host = config.get('remote-host') or 'localhost', config.get('remote-port') or 8000
        self.factory = GameServerFactory(self) if player == 1 else GameClientFactory(self)
        if player == 1: reactor.listenTCP(host[1], self.factory)
        elif player == 2: reactor.connectTCP(*host, self.factory)

    def p(self, s):
        logging.error(s)

    def main(self):
        logging.debug('Running gamespace main function')
        d = LoopingCall(main_game_loop, (self)).start(1. / self.tick)
        d.addBoth(self.p)
        reactor.run()

    def push_network_data(self, data):
        logging.info('Got network data: %s', data)

def main_game_loop(gs):

    # gs.clock.tick(self.tick)
    events = pygame.event.get()

    # Do backgrounds
    gs.screen.fill((0, 0, 0))

    for bg in gs.backgrounds: gs.screen.blit(*bg)
    gs.controls.update(events)
    gs.controls.draw(gs.screen)

    gs.module.game_loop(gs, events)

    for e in events:
        try:
            gs.factory.connection.transport.write('hello {}'.format(e.type).encode('latin-1'))
        except AttributeError:
            pass
        if e.type == pygame.KEYDOWN and gs.keymap.get(e.key) == 'menu':
            gs.module = sys.modules[__name__]

    pygame.display.flip()

def game_loop(gs, events):
    gs.menu.update(events)
    gs.screen.blit(*gs.menu_img)
    gs.menu.draw(gs.screen)

