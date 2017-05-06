#!/usr/bin/env python3

'''
modules/pacman.py

Pacman minigame.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame
from . import _render as render

class SpriteSheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])\
            for x in range(image_count)]
        return self.images_at(tups, colorkey)

class PacmanGame(object):
    def __init__(self):
        self.sprites      = SpriteSheet('./assets/sprites/sprites.jpg')
        self.pacman_strip = self.sprites.load_strip( (0, 0, 21, 21), 2 )
        self.frame_cursor = 0

    def game_loop(self, gs, events):
        # self.bg = pygame.image.load('./assets/maze_blank.jpg')
        # self.bg = pygame.transform.scale(self.bg, (gs.width, self.bg.get_height()))

        gs.screen.blit(self.pacman_strip[self.frame_cursor], (0, 0))
        self.frame_cursor = (self.frame_cursor + 1) % len(self.pacman_strip)

        # self.frame_cursor = 0
        # gs.screen.blit(self.pacman_strip[self.frame_cursor], (20, 20))
        # self.frame_cursor = self.frame_cursor + 1 % len(self.pacman_strip)

name   = 'pacman'
G_PACMAN = PacmanGame()

@render.render_controls
def game_loop(gs, events):
    '''Main execution/ game loop'''

    G_PACMAN.game_loop(gs, events)

    # gs.screen.blit(bg, bg.get_rect())

    # img = sprites.image_at(pacman_strip[frame_cursor])
    # gs.screen.blit(img, (100, 100))
    # frame_cursor += 1

class AnimatedGameObj(pygame.sprite.Sprite):
    '''Like GameObj but updates to next frame with each tick'''

    rotmap = { 'up': 90, 'left': 180, 'down': 270, 'right': 0, 'default': 0 }
    dirmap = { 'up': (0, -1), 'left': (-1, 0), 'down': (0, 1), 'right': (1, 0), 'default': (1, 0) }

    def __init__(self, fname, x=0, y=0, rotation=0, keymap={}):
        pygame.sprite.Sprite.__init__(self)

        # self.frames       = frames
        # self.frame_cursor = 0
        self.fname  = fname
        self.state  = 'default'
        self.keymap = keymap

        self.pos = self.x, self.y = x, y

    def update(self, events):
        '''Respond to pygame events'''
        self.frame_cursor = (self.frame_cursor + 1) % len(self.frames)
        for e in events:
            if e.type == pygame.KEYDOWN\
                    and self.keymap.get(e.key) in AnimatedGameObj.rotmap:
                self.state = self.keymap.get(e.key)
        self.update_obj(self.pos)

    def update_obj(self, pos):
        self.pos   = ( self.pos[0] + AnimatedGameObj.dirmap.get(self.state)[1]
                     , self.pos[1] + AnimatedGameObj.dirmap.get(self.state)[1] )
        # self.image = pygame.image.load(self.frames[self.frame_cursor])
        self.image = gif.GIFImage(self.fname)
        self.image = pygame.transform.rotate(self.image, AnimatedGameObj.rotmap.get(self.state))
        self.rect  = self.image.get_rect()
        self.rect.move_ip(*self.pos)

