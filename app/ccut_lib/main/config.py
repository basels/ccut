'''
The Config class includes defines that can be pre-defined
and are used in the project.
'''

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATA_DIR = 'data/'
    DATA_QUDT_V1_ONTO_FILES = ['unit.owl']
    DATA_USER_DEFINED_UNITS_FILE = 'user_defined.json'
    DATA_DIMENSIONS_MAP_FILE = 'quantity_dimension.json'