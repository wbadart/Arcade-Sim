#!/usr/bin/env python3

'''
' main.cpp
'
' Main execution of arcade sim projet.
'
' Brittany DiGenova
' Will Badart
' created: APR 2017
'''

import getopt
import pygame
import sys

G_KEEP_LOOPING = True

def usage(status=0):
    print('''usage: {} [ -w WIDTH -h HEIGHT ]
    -w WIDTH --width=WIDTH       Set the game window width (default: 640)
    -h HEIGHT --height=HEIGHT    Set the game window height (default: 480)
    --help                       Show this help message.'''.format(sys.argv[0])
    , file=sys.stderr)
    sys.exit(status)

def main( WIDTH=640
        , HEIGHT=480 ):

    pygame.init()

    if __name__ == '__main__':
        try:
            opts, args = getopt.getopt( sys.argv[1:], 'w:h:'
                                      , ['width=', 'height=', 'help'] )
        except getopt.GetoptError as e:
            print(e)

        for o, a in opts:
            if   o == '--width'  or o == '-w': WIDTH  = int(a)
            elif o == '--height' or o == '-h': HEIGHT = int(a)
            elif o == '--help': usage(0)

    size   = WIDTH, HEIGHT
    black  = 0, 0, 0
    screen = pygame.display.set_mode(size)

    title = pygame.transform.scale(pygame.image.load('assets/menu_bg.jpg'), size)
    title_rect = title.get_rect()
    while G_KEEP_LOOPING:
        loop_events = pygame.event.get()
        screen.fill(black)
        screen.blit(title, title_rect)
        pygame.display.flip()

if __name__ == '__main__': main()

