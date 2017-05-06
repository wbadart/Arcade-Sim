#!/usr/bin/env python3

'''
gameobj.py

Wrapper class to pygame sprite class.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging
import pygame

class GameObj(pygame.sprite.Sprite):
    '''
    Main export, wraps pygame sprite class. Edit at will, just make sure you
    keep the `update` method and `image` and `rect` properties (these are used
    by `Group`s.
    '''

    def __init__(self, states, x=0, y=0, keymap={}):
        '''Set initial configuration'''
        logging.info('Constructing GameObj at (%d, %d)', x, y)
        pygame.sprite.Sprite.__init__(self)

        self.states  = states
        self.state   = 'default'
        self.keymap  = keymap

        self.pos = self.x, self.y = x, y
        self.update_obj(self.pos)

    def update(self, events=[]):
        '''
        Default update function. Advances state machine to next state based
        on input key (as defined in the `states` dictionary
        '''
        for e in events:
            if e.type == pygame.KEYDOWN and self.keymap.get(e.key) in self.states:
                self.state = self.keymap.get(e.key)
            elif e.type == pygame.KEYUP: self.state = 'default'
        self.update_obj(self.pos)


    def update_obj(self, pos):
        '''Reset GameObj surface and rectangle based on current state'''
        self.image = pygame.image.load(self.states.get(self.state))
        self.rect  = self.image.get_rect()
        self.rect.move_ip(*pos)

class Button(pygame.sprite.Sprite):
    '''Class to represent menu buttons (separate from the A/B buttons).'''

    width  = 420
    height = 112
    size   = width, height

    def __init__(self, text, module, x=0, y=0, active=False):
        '''Construct button object and set state.'''
        pygame.sprite.Sprite.__init__(self)

        self.text     = text
        self.module   = module
        self.pos      = self.x, self.y = x, y
        self.active   = active
        self.font     = pygame.font.SysFont('Helvetica', 75)
        self.update()

    def update(self):
        '''Set object properties (basically color) based on `self.active`'''
        self.color = (0, 0, 0) if self.active else (255, 255, 255)
        self.label = self.font.render(self.text, 10, self.color)

        self.bg_color = (255, 255, 255) if self.active else (0, 0, 0)
        self.bg       = pygame.Surface(Button.size)
        self.rect     = self.bg.get_rect()
        self.rect.move_ip(self.pos)
        self.bg.fill(self.bg_color)

    def draw(self, screen):
        '''Blit the button to the screen at `self.pos`'''
        screen.blit(self.bg, self.rect)
        screen.blit(self.label, self.pos)

    def click(self, gs):
        gs.module = self.module

    def set_state(self, state):
        '''Turns the button on or off'''
        self.active = state

class Menu(object):
    '''Basically a container of buttons'''

    def __init__(self, buttons, gs, x=0, y=0, keymap={}):
        '''Set initial configuration'''
        self.buttons = buttons
        self.gs      = gs
        self.pos     = self.x, self.y = x, y
        self.keymap  = keymap
        # Cursor is used to track the active button
        self.cursor  = 0
        self.set_active()

    def update(self, events=[]):
        '''Change the active menu item based on key'''
        for e in (e for e in events if e.type == pygame.KEYDOWN):
            if self.keymap.get(e.key) == 'down':
                self.cursor = (self.cursor + 1) % len(self.buttons)
                logging.info('Moving cursor to %d', self.cursor)
            elif self.keymap.get(e.key) == 'up':
                self.cursor = self.cursor - 1 if self.cursor else len(self.buttons) - 1
                logging.info('Moving cursor to %d', self.cursor)
            elif self.keymap.get(e.key) == 'A':
                self.active_button.click(self.gs)

        self.set_active()

    def set_active(self):
        '''Toggle state of member buttons based on position of `cursor`'''
        for i, b in enumerate(self.buttons): b.set_state(self.cursor == i)
        self.active_button = self.buttons[self.cursor]

    def draw(self, screen):
        '''Render member buttons to passed screen'''
        for i, b in enumerate(self.buttons):
            b.pos = self.x, self.y + i * (Button.height + 5)
            b.update()
            b.draw(screen)

