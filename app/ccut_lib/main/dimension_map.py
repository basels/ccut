import json

# Singleton class
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
        # TODO: Move path to config file
        with open("data/quantity_dimension.json") as f:
            self.qd_map = json.load(f)
