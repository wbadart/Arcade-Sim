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

    def render_main(gs):
        gs.clock.tick(gs.tick)
        gs.screen.fill((0, 0, 0))

        gs.screen.blit(*gs.screen_bg)
        gs.screen.blit(*gs.control_bg)

        loop_events = pygame.event.get()
        gs.controlobjs.update(loop_events)
        gs.controlobjs.draw(gs.screen)

        render_submodule(gs, loop_events)

        pygame.display.flip()


    return render_main


