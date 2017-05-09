#!/usr/bin/env python3

'''
gamespace.py

Over-arching class to wrap pygame functionality.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging
import modules._misc   as misc
import modules._render as render
import os
import pygame

from gameobj import *
from loader  import ModuleLoader
from players import *

from twisted.internet.protocol  import Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint

class GameSpace(object):
    '''The main export. Contains configuration and main execution for pygame.'''

    def __init__(self, player, config={}):
        '''Construct GameSpace and perform pygame initialization'''

        # Initialize pygame library
        pygame.init()
        self.config       = config
        self.network_data = []
        self.multiplayer  = False if player == 1 else True

        # Configure and open the window
        self.size   = self.width, self.height = config.get('width'), config.get('height')
        self.screen = pygame.display.set_mode(self.size)
        self.tick   = config.get('tick')

        # Configure keymapping; this establishes a mapping from the "command" (up/
        # down/etc, keys of the config keymap) to the corresponding pygame key const
        # Ultimately maps ascii_code -> command
        self.keymap  = { ord(self.config['keymap'].get(c)): c for c in self.config['keymap'] }
        logging.info('Established keymap: %s', self.keymap)

        # Misc. game properties
        self.clock  = pygame.time.Clock()

        # Bring in the module loader
        self.loader = ModuleLoader('./config.yml')
        self.module = self
        self.help_module = self.loader.load_individual('modules.help')

        # Initialize main menu screen
        self.screen_bg = pygame.Surface((self.width, self.width))
        self.screen_bg.fill((0, 0, 0))
        self.screen_bg = self.screen_bg, self.screen_bg.get_rect()

        self.control_bg = pygame.Surface((self.width, self.height - self.width))
        self.control_bg.fill((45, 45, 45))
        self.control_bg = self.control_bg, self.control_bg.get_rect()
        self.control_bg[1].move_ip(0, self.width)

        menu_img  = pygame.image.load('./assets/menu_bg.jpg')
        menu_rect = menu_img.get_rect()

        scale_factor  = self.width / menu_rect.width
        menu_img      = pygame.transform.scale(menu_img, (self.width, self.screen_bg[1].height))
        menu_rect     = menu_img.get_rect()
        self.menu_img = menu_img, menu_rect

        # Fonts and stuff
        self.fonts         = { 'title': pygame.font.SysFont('Helvetica', 16) }
        help_key, menu_key = chr(next(k for k in self.keymap if self.keymap[k] == 'help'))\
                           , chr(next(k for k in self.keymap if self.keymap[k] == 'menu'))
        self.help_label    = self.fonts['title'].render( 'Press \'{}\' for help, \'{}\' to return to menu.'\
                                                    .format(help_key, menu_key)
                                                    , 10, (160, 160, 160))
        self.help_label = self.help_label, self.help_label.get_rect()
        self.help_label[1].move_ip((self.width / 2 - self.help_label[1].width / 2
                                  , self.height - self.help_label[1].height ))

        self.controlobjs = pygame.sprite.RenderPlain(
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
                                  }, self.width / 2 + 168, self.width + 20, self.keymap )
                        ] )

        self.menu = Menu( [ Button(m.name, m, not i) for i, m in enumerate(self.loader.modules) ]
                        , self, self.width / 2 - Button.width / 2, 10, self.keymap )

        host = 'localhost', 8000
        from twisted.internet import reactor

        if player == 1:

            logging.info('P1 listening on port %d', host[1])
            self.factory = Player1ServerFactory(self)
            #self.factory = Player2ClientFactory(self)
            #reactor.connectTCP('ash.campus.nd.edu', 40007, self.factory)
            TCP4ServerEndpoint(reactor, host[1]).listen(self.factory)

        else:

            logging.info('P2 attempting connection to %s:%d', *host)
            self.factory = Player2ClientFactory(self)
            #reactor.connectTCP('ash.campus.nd.edu', 40019, self.factory)
            TCP4ClientEndpoint(reactor,'localhost', 8000).connect(self.factory)

        pid = os.fork()
        if pid == 0: reactor.run()


    def main(self):
        '''Main game execution. Basically a wrapper for `game_loop`'''
        try:
            while True:
                loop_events = pygame.event.get()
                self.module.game_loop(self, loop_events, self.network_data)
        except KeyboardInterrupt as e:
            print('Bye!')
        except misc.Loss as e:
            while True: loss_loop(self, [])

    def game_loop(self, gs, events, network_data):
        game_loop(gs, events, network_data)

    def on_datareceived(self, data):
        self.network_data.append(data)

@render.render_controls
def game_loop(gs, events, network_data):
    '''Main execution/ game loop'''

    gs.screen.blit(*gs.menu_img)
    gs.menu.update(events)
    gs.menu.draw(gs.screen)

    for e in (e for e in events if e.type == pygame.KEYDOWN and gs.keymap.get(e.key) == 'help'):
        gs.module = gs.help_module

@render.render_controls
def loss_loop(gs, events, net_data=[]):
    menu_img = pygame.image.load('./assets/gameover.jpg')
    scale_factor  = gs.width / menu_img.get_width()
    menu_img      = pygame.transform.scale(menu_img, (gs.width, gs.screen_bg[1].height))
    gs.screen.blit(menu_img, menu_img.get_rect())


