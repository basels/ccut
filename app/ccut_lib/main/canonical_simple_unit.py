from main.unit_match import UnitMatch
from main.unit import Unit
from main.symbol_map import SymbolMap
from main.dimension_map import DimensionMap

QUDT_V1_FIXED_ONTOLOGY_PREF = "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#"

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
        self.unit_obj['qudtp:symbol'] = self.unit.symbol

    def set_quantity(self, qudt_unit):
        if qudt_unit is not None:
            self.unit_obj['qudtp:quantityKind'] =  QUDT_V1_FIXED_ONTOLOGY_PREF + qudt_unit['uri'].split('#')[1]
            if qudt_unit['prefix'] is not None:
                self.unit_obj['ccut:prefix'] = QUDT_V1_FIXED_ONTOLOGY_PREF + qudt_unit['prefix'].split('#')[1]
                self.unit_obj['ccut:prefixConversionMultiplier'] = qudt_unit['prefix_conversion_multiplier']
                self.unit_obj['ccut:prefixConversionOffset'] = qudt_unit['prefix_conversion_offset']
        else:
            self.unit_obj['qudtp:quantityKind'] = "UNKNOWN TYPE"

    def set_multiplier(self):
        if self.unit.multiplier is not None:
            self.unit_obj['ccut:multiplier'] = self.unit.multiplier

    def set_exponent(self):
        if self.unit.exponent is not None:
            self.unit_obj['ccut:exponent'] = self.unit.exponent

    def set_dimension(self, qudt_unit):
        if qudt_unit is None:
            self.unit_obj['ccut:hasDimension'] = "UNKNOWN DIMENSION"
        else:
            quantityKindUri = qudt_unit['quantityKind']
            quantityKind = quantityKindUri.rsplit("#")[1]
            dimension = self.quantityDimensionMap.qd_map[quantityKind]
            if dimension == '':
                dimension = "DIMENSION NOT IN MAPPING"
            self.unit_obj['ccut:hasDimension'] = dimension

    def set_conversion_params(self, qudt_unit):
        if qudt_unit is not None:
            self.unit_obj['qudtp:conversionMultiplier'] = qudt_unit['conversion_multiplier']
            self.unit_obj['qudtp:conversionOffset'] = qudt_unit['conversion_offset']
        else:
            self.unit_obj['qudtp:conversionMultiplier'] = self.unit_obj['qudtp:conversionOffset'] = None

