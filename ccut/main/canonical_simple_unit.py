'''
The CanonicalSimpleUnit class wraps the Unit class
and binds it to a dimension.
'''

from .dimension_map import DimensionMap
from .symbol_map import SymbolMap, INDEX_NAME_URI, INDEX_NAME_PREFIX, INDEX_NAME_QUANTITYKIND, \
                            INDEX_NAME_CONVERSION_MULTIPLIER, INDEX_NAME_CONVERSION_OFFSET, \
                            INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER, INDEX_NAME_PREFIX_CONVERSION_OFFSET
from .unit import Unit
from .unit_match import UnitMatch

QUDT_V1_NAMESPACE_INVALID = 'http://data.nasa.gov/qudt/owl/unit#'
QUDT_V1_NAMESPACE_VALID = 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#'
QUDT_PROPERTIES_NAMESPACE = 'qudtp'
CCUT_NAMESPACE = 'ccut'

def fix_qudt_namespace_if_exists(original_uri):
    new_uri = original_uri.replace(QUDT_V1_NAMESPACE_INVALID, QUDT_V1_NAMESPACE_VALID)
    return new_uri

class CanonicalSimpleUnit:
    def __init__(self, unit: Unit):
        self.unit = unit
        self.unit_obj = dict()
        self.symbol_map_instance = SymbolMap.get_instance()
        self.quantityDimensionMap = DimensionMap.get_instance()

        qudt_unit = UnitMatch.find_best_unit_match(unit.symbol, self.symbol_map_instance)
        self.set_symbol()
        self.set_quantity(qudt_unit)
        self.set_dimension(qudt_unit)
        self.set_conversion_params(qudt_unit)

        self.set_multiplier()
        self.set_exponent()

    def get_unit_object(self):
        return self.unit_obj

    def set_symbol(self):
        self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:symbol'] = self.unit.symbol

    def set_quantity(self, qudt_unit):
        if qudt_unit is not None:
            self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind'] = fix_qudt_namespace_if_exists(qudt_unit[INDEX_NAME_URI])
            if qudt_unit[INDEX_NAME_PREFIX] is not None:
                self.unit_obj[f'{CCUT_NAMESPACE}:prefix'] = fix_qudt_namespace_if_exists(qudt_unit[INDEX_NAME_PREFIX])
                self.unit_obj[f'{CCUT_NAMESPACE}:prefixConversionMultiplier'] = qudt_unit[INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER]
                self.unit_obj[f'{CCUT_NAMESPACE}:prefixConversionOffset'] = qudt_unit[INDEX_NAME_PREFIX_CONVERSION_OFFSET]
        else:
            self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind'] = "UNKNOWN TYPE"

    def set_multiplier(self):
        if self.unit.multiplier is not None:
            self.unit_obj[f'{CCUT_NAMESPACE}:multiplier'] = self.unit.multiplier

    def set_exponent(self):
        if self.unit.exponent is not None:
            self.unit_obj[f'{CCUT_NAMESPACE}:exponent'] = self.unit.exponent

    def set_dimension(self, qudt_unit):
        if qudt_unit is None:
            self.unit_obj[f'{CCUT_NAMESPACE}:hasDimension'] = "UNKNOWN DIMENSION"
        else:
            quantityKindUri = qudt_unit[INDEX_NAME_QUANTITYKIND]
            quantityKind = quantityKindUri.rsplit("#")[1]
            dimension = self.quantityDimensionMap.qd_map[quantityKind]
            if dimension == '':
                dimension = "DIMENSION NOT IN MAPPING"
            self.unit_obj[f'{CCUT_NAMESPACE}:hasDimension'] = dimension

    def set_conversion_params(self, qudt_unit):
        if qudt_unit is not None:
            self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier'] = qudt_unit[INDEX_NAME_CONVERSION_MULTIPLIER]
            self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset'] = qudt_unit[INDEX_NAME_CONVERSION_OFFSET]
        else:
            self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier'] = self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset'] = None

