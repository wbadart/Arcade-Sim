#!/usr/bin/env python3

'''
modules/snake.py

The classic.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import logging
import pygame

from random import randrange

name = 'snake'

def get_snake_color():
    return randrange(80, 255), randrange(80, 255), randrange(80, 255)
def get_snake_start_pos():
    logging.debug('Generating starting position')
    return randrange(250, 500), randrange(250, 500)

class SnakeCell(pygame.sprite.Sprite):

    dimensions = 30, 30

    def __init__(self, pos, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.pos   = pos
        self.image = pygame.Surface(SnakeCell.dimensions)
        self.rect  = self.image.get_rect()
        self.rect.move_ip(self.pos)
        self.image.fill(color)

    def draw(self, screen):
        screen.blit(self.image, self.pos)

class Snake(object):

    start_len = 2

    def __init__(self):
        self.color = get_snake_color()
        self.pos   = get_snake_start_pos()

        self.data  = [ SnakeCell((self.pos[0] - SnakeCell.dimensions[0] * i, self.pos[1])
                                , self.color) for i in range(Snake.start_len) ]

        self.states = { 'up': (0, -SnakeCell.dimensions[1] / 5)
                      , 'down': (0, SnakeCell.dimensions[1] / 5)
                      , 'right': (SnakeCell.dimensions[0] / 5, 0)
                      , 'left' : (-SnakeCell.dimensions[0] / 5, 0) }
        self.state    = 'right'

    def update(self, gs, events):

        for e in (e for e in events if e.type == pygame.KEYDOWN):
            self.state = gs.keymap.get(e.key) or self.state

        delta = self.states.get(self.state)
        self.data.insert(0, SnakeCell(( self.data[0].rect.x + delta[0]
                                      , self.data[0].rect.y + delta[1]
                                     ), self.color ))
        if self.data[0].rect.colliderect(SnakeGame.food.rect):
            SnakeGame.points += 1
            SnakeGame.food = SnakeCell((randrange(0, 600, 30), randrange(0, 600, 30)))
        elif self.data[0].rect.collidelist(self.data[5:]) != -1:
            raise Exception('Game over')
        else: self.data.pop()

    def draw(self, screen):
        pygame.sprite.RenderPlain(self.data).draw(screen)

    def out_of_bounds(self):
        x, y = self.data[0].rect.x, self.data[0].rect.y
        return (x < 0 or x >= 640) or (y < 0 or y >= 640)


class SnakeGame(object):

    food   = SnakeCell((randrange(0, 600, 30), randrange(0, 600, 30)))
    points = 0

    def __init__(self, multiplayer):
        self.snakes = [ Snake() for _ in range(multiplayer + 1) ]

    def game_loop(self, gs, events, net_queue):

        SnakeGame.food.draw(gs.screen)
        self.snakes[0].update(gs, events)
        self.snakes[1].update(gs, net_queue)

        self.snakes[0].draw(gs.screen)
        self.snakes[1].draw(gs.screen)

game = SnakeGame(True)
def game_loop(gs, events, net_queue):
    game.game_loop(gs, events, net_queue)


