#!/usr/bin/env python3

'''
modules/snake.py

The classic.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame
from random import randrange
from . import _misc   as misc
from . import _render as render

name = 'snake'

class SnakeCell(pygame.sprite.Sprite):
    def __init__(self, pos, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect  = self.image.get_rect()
        self.rect.move_ip(pos)

class SnakeGame(object):

    colors = (randrange(80, 255), randrange(80, 255),randrange(80, 255))\
           , (randrange(80, 255), randrange(80, 255),randrange(80, 255))

    food = SnakeCell((randrange(0, 600, 30), randrange(0, 600, 30)))
    points = 0

    def __init__(self, player=1):
        self.main_snake = Snake(player)

    def game_loop(self, gs, events):
        gs.screen.blit(SnakeGame.food.image, SnakeGame.food.rect)
        self.main_snake.update(gs, events)
        self.main_snake.draw(gs.screen)


class Snake(object):
    def __init__(self, player=1):
        self.color = SnakeGame.colors[0 if player == 1 else 1]

        self.data  = [ SnakeCell((250, 250) if player == 1 else (450, 250), self.color)
                     , SnakeCell((220, 250) if player == 1 else (420, 250), self.color) ]

        self.group = pygame.sprite.RenderPlain(self.data)
        self.player = player
        self.state = 'right'
        self.states = { 'up': (0, -30),
                        'down': (0, 30),
                        'right': (30, 0),
                        'left' : (-30, 0)}

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
def game_loop(gs, events):
    '''Main execution/ game loop'''
    G_SNAKE.game_loop(gs,events)

