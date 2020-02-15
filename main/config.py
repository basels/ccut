'''
The Config class includes defines that can be pre-defined
and are used in the project.
'''

from os import environ, path, pardir

class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATA_DIR = f'{path.abspath(path.join(path.dirname(__file__), pardir))}/data/'
    DATA_QUDT_V1_ONTO_FILES = ['unit.owl']
    DATA_USER_DEFINED_UNITS_FILE = 'user_defined.json'
    DATA_DIMENSIONS_MAP_FILE = 'quantity_dimension.json'
    DATA_LABELS_EXTENSION_MAP_FILE = 'labels_extension.json'
    DATA_PRE_DEFINED_PRIO_FILE = 'uri_prios.json'