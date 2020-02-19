from ..main.unit_match import UnitMatch
from ..main.symbol_map import SymbolMap


def test():

    s = SymbolMap.get_instance()

    assert UnitMatch.find_best_unit_match('km', s) == \
            {'uri': 'http://data.nasa.gov/qudt/owl/unit#Meter', 'quantityKind': 'http://data.nasa.gov/qudt/owl/quantity#Length', \
             'prefix': 'http://data.nasa.gov/qudt/owl/unit#Kilo', 'conversion_multiplier': 1, 'conversion_offset': 0, \
             'prefix_conversion_multiplier': 1000, 'prefix_conversion_offset': 0}
    assert UnitMatch.find_best_unit_match('kilometer', s) == \
            {'uri': 'http://data.nasa.gov/qudt/owl/unit#Meter', 'quantityKind': 'http://data.nasa.gov/qudt/owl/quantity#Length', \
            'prefix': 'http://data.nasa.gov/qudt/owl/unit#Kilo', 'conversion_multiplier': 1, 'conversion_offset': 0, \
             'prefix_conversion_multiplier': 1000, 'prefix_conversion_offset': 0}
    assert UnitMatch.find_best_unit_match('ms', s) == \
            {'uri': 'http://data.nasa.gov/qudt/owl/unit#SecondTime', 'quantityKind': 'http://data.nasa.gov/qudt/owl/quantity#Time', \
            'prefix': 'http://data.nasa.gov/qudt/owl/unit#Milli', 'conversion_multiplier': 1, 'conversion_offset': 0, \
            'prefix_conversion_multiplier': 0.001, 'prefix_conversion_offset': 0}
