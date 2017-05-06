#!/usr/bin/env python3

'''
main.py

Main execution for Arcade-Sim.

Contributors:
    - Brittany DiGenova (bdigenov)
    - Will Badart       (wbadart)
created: MAY 2017

usage: main.py [ OPTIONS ]

Options:
    -c FILE   --config FILE     Use FILE as the program config file (default: ./config.yml)
    -v        --verbose         Set the program log level to DEBUG (default: WARNING)
    -p PLAYER                   Set player number to PLAYER (must be 1 or 2; required)
    --help                      Show this help message
'''

import getopt
import logging
import sys
import yaml

from gamespace import GameSpace

#======================
# Command line helpers
#======================

def usage(status=0):
    '''Print the help message and exit with exit code `status`'''
    print(__doc__, file=sys.stderr)
    sys.exit(status)

#================
# Main execution
#================

def main( CONFIG_FNAME='./config.yml', LOG_LEVEL=logging.INFO ):
    '''Run main execution, launch game window and play!'''

    # Parse command line options
    PLAYER = None
    try:
        opts, args = getopt.getopt( sys.argv[1:], 'p:c:vh'
                                  , ['config=', 'verbose', 'help'] )
        for o, a in opts:
            if   o == '--config' or o == '-c': CONFIG_FNAME = a
            elif o == '--verbose' or o == '-v': LOG_LEVEL = logging.DEBUG
            elif o == '-p': PLAYER = int(a)
            elif o == '--help': usage()
    except getopt.GetoptError as e:
        logging.error(e)
        sys.exit(1)
    except ValueError as e:
        logging.error('PLAYER, WIDTH, and HEIGHT require valid integer arguments')
        sys.exit(1)

    # Set inital config
    config = {}
    with open(CONFIG_FNAME, 'r') as fs:
        config = yaml.safe_load(fs)

    logging.basicConfig( level=LOG_LEVEL
                       , format='[%(module)s][%(levelname)s]:%(message)s' )

    # Run game loop
    game = GameSpace(player, config)
    game.main()

if __name__ == '__main__': main()

