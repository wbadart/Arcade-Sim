#!/usr/bin/env python3

'''
' gameobj.py
'
' Extension of Pygame sprite class for rendering stuff.
'
' Brittany DiGenova
' Will Badart
' created: APR 2017
'''

import pygame

class GameObj(pygame.sprite.Sprite):

    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.image.load(path)
        self.rect    = self.surface.get_rect()

