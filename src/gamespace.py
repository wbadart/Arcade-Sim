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

from gameobj import *
from loader import ModuleLoader

class GameSpace(object):
    '''The main export. Contains configuration and main execution for pygame.'''

    def __init__(self, config={}):
        '''Construct GameSpace and perform pygame initialization'''

        # Initialize pygame library
        pygame.init()
        self.config = config

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
        print('LOADER MODULES:', self.loader.modules)
        self.module = self

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

        scale_factor = self.width / menu_rect.width
        menu_img  = pygame.transform.scale(menu_img, (self.width, self.screen_bg[1].height))
        menu_rect = menu_img.get_rect()
        self.menu_img = menu_img, menu_rect

        # Fonts and stuff
        self.fonts      = { 'title': pygame.font.SysFont('Helvetica', 75) }
        self.menu_label = self.fonts['title'].render('Main menu', 10, (255, 255, 255))

        self.gameobjs = pygame.sprite.RenderPlain(
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
    def main(self):
        '''Main game execution. Basically a wrapper for `game_loop`'''
        try:
            while True: self.module.game_loop(self)
        except KeyboardInterrupt as e:
            print('Bye!')

    def game_loop(self, gs=None):
        '''Main execution/ game loop'''

        # Tick regulation
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))

        self.screen.blit(*self.screen_bg)
        self.screen.blit(*self.control_bg)
        self.screen.blit(*self.menu_img)
        # self.screen.blit(*self.menu)
        # self.screen.blit(self.menu_label, (self.screen.get_width() / 2 - self.menu_label.get_width() / 2, 100))

        # Handle events
        loop_events = pygame.event.get()
        self.gameobjs.update(loop_events)
        self.gameobjs.draw(self.screen)

        self.menu.update(loop_events)
        self.menu.draw(self.screen)


        # Render screen
        pygame.display.flip()

