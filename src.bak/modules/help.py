#!/usr/bin/env python3

'''
help.py

Submodule that display help menu.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame
from . import _render as render

name = 'help'

@render.render_controls
def game_loop(gs, events):
    '''Game loop to show help menu'''

    B_key      = chr(next((k for k in gs.keymap if gs.keymap[k] == 'B')))
    help_str   = ['{} - {}'.format(gs.keymap[k], chr(k)) for k in gs.keymap]\
               + ['Press \'{}\' to return.'.format(B_key)]
    labels     = [gs.fonts['title'].render(s, 10, (255, 255, 255)) for s in help_str]

    for i, l in enumerate(labels):
        gs.screen.blit(l, (gs.width / 2 - l.get_width() / 2, 20 + i * l.get_height()))

    for e in (e for e in events if e.type == pygame.KEYDOWN and gs.keymap.get(e.key) == 'B'):
        gs.module = gs

