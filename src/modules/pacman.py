#!/usr/bin/env python3

'''
modules/pacman.py

Pacman minigame.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame
from . import render

name = 'pacman'

@render.render_controls
def game_loop(gs, events):
    '''Main execution/ game loop'''

    img = pygame.Surface((gs.width, gs.width))
    img.fill((200, 10, 10))
    rect = img.get_rect()
    gs.screen.blit(img, rect)

    pygame.display.flip()

