#!/usr/bin/env python3

'''
loader.py

Used to load in the individual game modules.

Brittany DiGenova
Will Badart

created: MAY 2017
'''

import importlib
import logging
import yaml

class ModuleLoader(object):
    '''
    The ModuleLoader class finds mini-game modules specified in the
    config file and plugs them into pygame.
    '''

    def __init__(self, config_filename='./config.yml'):
        '''Construct Loader, parsing options from config file'''

        # Load the config file
        config = {}
        with open(config_filename, 'r') as fs:
            config = yaml.safe_load(fs)

        # Sanity checks
        if 'modules' not in config:
            logging.error('Config missing required field "modules".')
        if 'module-root' not in config:
            config['module-root'] = 'modules'

        # Load them modules
        self.modules = []
        for m in config['modules']:
            try:
                self.modules.append(importlib.import_module(
                    '{}.{}'.format(config['module-root'], m)) )
            except ImportError as e:
                logging.error(e)

    def load_individual(self, module_name):
        '''Load an individual module'''
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            logging.error(e)

