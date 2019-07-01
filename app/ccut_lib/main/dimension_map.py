'''
The DimensionMap is a singleton class to be accessed and used by the service.
It holds a map (dictionary) of dimensions ('qd_map').
'''

from json import load
from .config import Config

# Use as singleton class
class DimensionMap:
    instance = None

    def __init__(self):
        self.qd_map = dict()

        self.load_map()

    @staticmethod
    def get_instance() -> 'DimensionMap':
        if DimensionMap.instance is None:
            DimensionMap.instance = DimensionMap()

        return DimensionMap.instance

    def load_map(self):
        with open(f'{Config.DATA_DIR}/{Config.DATA_DIMENSIONS_MAP_FILE}') as f:
            self.qd_map = load(f)
