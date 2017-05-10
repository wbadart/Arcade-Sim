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
import logging
import pygame
import sys

from gameobj import GameObj

G_KEEP_LOOPING = True
G_MAIN_LOGGER  = logging.getLogger('G_MAIN_LOGGER')
G_GAME_OBJS    = {}

def usage(status=0):
    '''Display the usage message end exit with exit code `status`'''

    print('''usage: {} [ -w WIDTH -h HEIGHT ]
    -w WIDTH --width=WIDTH       Set the game window width (default: 640)
    -h HEIGHT --height=HEIGHT    Set the game window height (default: 480)
    --help                       Show this help message.'''.format(sys.argv[0])
    , file=sys.stderr)
    sys.exit(status)

def error(e, status=1):
    '''Use the global logger to log an error and exit with exit code `status`'''

    G_MAIN_LOGGER.error(e)
    usage(status)

def game_loop(screen, black=(0, 0, 0)):
    '''Main game execution'''

    font = pygame.font.SysFont('Helvetica', 75)
    label = font.render('Main menu', 10, (255, 255, 255))
    loop_events = pygame.event.get()
    screen.fill(black)
    for obj in G_GAME_OBJS.values():
        # obj.tick(loop_events)
        screen.blit(obj.surface, obj.rect)
    screen.blit(label, (screen.get_width() / 2 - label.get_width() / 2, 100))
    pygame.display.flip()

def main( WIDTH=640
        , HEIGHT=480
        , LOG_LEVEL=logging.INFO ):
    '''Main program execution, including command line parsing'''

    pygame.init()

    if __name__ == '__main__':
        opts, args = None, None
        try:
            opts, args = getopt.getopt( sys.argv[1:], 'w:h:v'
                                      , ['width=', 'height=', 'verbose', 'help'] )
        except getopt.GetoptError as e:
            error(e)

        for o, a in opts:
            if   o == '--width'  or o == '-w': WIDTH  = int(a)
            elif o == '--height' or o == '-h': HEIGHT = int(a)
            elif o == '--verbose' or o == '-v': LOG_LEVEL = logging.DEBUG
            elif o == '--help': usage(0)

    logging.basicConfig( level=LOG_LEVEL )
    G_MAIN_LOGGER.info('Using configuration: WIDTH=%d, HEIGHT=%d', WIDTH, HEIGHT)

    size   = WIDTH, HEIGHT
    black  = 0, 0, 0
    screen = pygame.display.set_mode(size)

    G_GAME_OBJS['title'] = GameObj('assets/menu_bg.jpg')
    G_GAME_OBJS['title'].surface = pygame.transform.scale(G_GAME_OBJS['title'].surface, size)

    while G_KEEP_LOOPING: game_loop(screen)

if __name__ == '__main__': main()

