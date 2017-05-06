#!/usr/bin/env python3

'''
modules/pacman.py

Duckhunt minigame.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame

name = 'duck hunt'

def game_loop(gs):
    '''Game loop for duck hunt game'''
    gs.clock.tick(gs.tick)
    gs.screen.fill((0, 0, 0))

    gs.screen.blit(*gs.screen_bg)
    gs.screen.blit(*gs.control_bg)

    loop_events = pygame.event.get()
    gs.gameobjs.update(loop_events)
    gs.gameobjs.draw(gs.screen)

    pygame.display.flip()

