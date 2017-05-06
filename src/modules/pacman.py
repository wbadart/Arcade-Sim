#!/usr/bin/env python3

'''
modules/pacman.py

Pacman minigame.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame

name = 'pacman'

def game_loop(gs):
    '''Main execution/ game loop'''

    # Tick regulation
    gs.clock.tick(gs.tick)
    gs.screen.fill((0, 0, 0))

    gs.screen.blit(*gs.screen_bg)
    gs.screen.blit(*gs.control_bg)

    # Handle events
    loop_events = pygame.event.get()
    gs.gameobjs.update(loop_events)
    gs.gameobjs.draw(gs.screen)

    img = pygame.Surface((gs.width, gs.width))
    img.fill((200, 10, 10))
    rect = img.get_rect()
    gs.screen.blit(img, rect)

    pygame.display.flip()

