#!/usr/bin/env python3

'''
modules/_render_main.py

Simple decorator to take care of rendering the repeated objects
shared by all submodules (controls and such)

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import pygame

def render_controls(render_submodule):
    '''Send all control modules (joystick and such) to screen'''

    def render_main(gs, events=[], network_data=[]):
        gs.clock.tick(gs.tick)
        gs.screen.fill((0, 0, 0))

        gs.screen.blit(*gs.screen_bg)
        gs.screen.blit(*gs.control_bg)
        gs.screen.blit(*gs.help_label)

        gs.controlobjs.update(events)
        gs.controlobjs.draw(gs.screen)

        render_submodule(gs, events, network_data)

        for e in (e for e in events if e.type == pygame.KEYDOWN and gs.keymap.get(e.key) == 'menu'):
            gs.module = gs

        pygame.display.flip()


    return render_main


