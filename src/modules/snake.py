#!/usr/bin/env python3

'''
modules/snake.py

The classic.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame
from collections import namedtuple
from random import randrange
from . import _misc   as misc
from . import _render as render

name  = 'snake'
ETYPE = namedtuple('ETYPE', 'type key')

def get_snake_color():
    return randrange(80, 255), randrange(80, 255), randrange(80, 255)
def get_snake_start_pos():
    return randrange(250, 500), randrange(250, 500)

def netdata2event(datastr):
    if ':' not in datastr: return ETYPE(type=None, key='')
    etype, ekey = data.string.split(':')
    return ETYPE(type=int(etype), key=int(ekey))

class SnakeCell(pygame.sprite.Sprite):
    def __init__(self, pos, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect  = self.image.get_rect()
        self.rect.move_ip(pos)

class SnakeGame(object):

    food   = SnakeCell((randrange(0, 600, 30), randrange(0, 600, 30)))
    points = 0

    def __init__(self):
        self.snakes = [ Snake() for _ in range(2) ]

    def game_loop(self, gs, events, network_data):

        try:
            network_data = [ netdata2event(network_data.pop()) ]
        except IndexError:
            network_data = []

        if gs.multiplayer:
            for e in (e for e in events if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP):
                gs.factory.write('{}:{}'.format(e.type, getattr(e, 'key')))

        gs.screen.blit(SnakeGame.food.image, SnakeGame.food.rect)
        self.snakes[0].update(gs, events)
        self.snakes[0].draw(gs.screen)

        if gs.multiplayer:
            self.snakes[1].update(gs, network_data)
            self.snakes[1].draw(gs.screen)


class Snake(object):
    def __init__(self):

        self.color = get_snake_color()
        self.data  = [ SnakeCell(get_snake_start_pos()) for _ in range(2) ]
        self.group = pygame.sprite.RenderPlain(self.data)

        self.states = { 'up': (0, -30), 'down': (0, 30), 'right': (30, 0), 'left' : (-30, 0) }
        self.state  = 'right'

    def update(self, gs, events):

        for e in (e for e in events if e.type == pygame.KEYDOWN):
            self.state = gs.keymap.get(e.key) or self.state

        x_movement = self.states.get(self.state)[0]
        y_movement = self.states.get(self.state)[1]
        self.data.insert(0, SnakeCell(( self.data[0].rect.x + x_movement, self.data[0].rect.y + y_movement ), self.color))

        if self.data[0].rect.colliderect(SnakeGame.food.rect):
            SnakeGame.points += 1
            SnakeGame.food = SnakeCell((randrange(0, 600, 30), randrange(0, 600, 30)))
        elif self.data[0].rect.collidelist(self.data[1:]) != -1:
            raise misc.Loss
        else: self.data.pop()

    def draw(self, surface):
        self.group = pygame.sprite.RenderPlain(self.data)
        self.group.draw(surface)

G_SNAKE = SnakeGame()

@render.render_controls
def game_loop(gs, events, network_data):
    '''Main execution/ game loop'''
    G_SNAKE.game_loop(gs, events, network_data)

