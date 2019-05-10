from main.rdf_parser import rdf_parser
from main.si_prefix import si_prefix
from main.qudt_unit import QudtUnit

QUDT_ONTOLOGY_DIR = 'data/'
QUDT_V1_ONTOLOGY_FILES = ['unit.owl']
# QUDT_V2_ONTOLOGY_FILES = ['VOCAB_QUDT-UNITS-BASE-v2.0.ttl', 'VOCAB_QUDT-UNITS-SPACE-AND-TIME-v2.0.ttl']

# Use as singleton class
class SymbolMap:

    instance = None

    def __init__(self):
        self.symbol_map = dict()
        self.label_map = dict()
        self.si_prefix_map = dict()

        for ontof in QUDT_V1_ONTOLOGY_FILES:
            self.rp = rdf_parser(QUDT_ONTOLOGY_DIR, ontof)

        self.construct_map()

    @staticmethod
    def get_instance() -> 'SymbolMap':
        if SymbolMap.instance is None:
            SymbolMap.instance = SymbolMap()

        return SymbolMap.instance

    def is_qudt_unit_with_si_prefix(self, qu: QudtUnit):
        # Return true for km, ms, etc
        # False for mX
        if not hasattr(qu, 'conversion_multiplier') or not hasattr(qu, 'symbol'):
            return False

        prefix, suffix = qu.symbol[0], qu.symbol[1:]
        conversion_factor = si_prefix.get_factor(prefix)
        if qu.conversion_multiplier == conversion_factor and suffix in self.symbol_map:
            return True

        prefix, suffix = qu.symbol[:2], qu.symbol[2:]
        conversion_factor = si_prefix.get_factor(prefix)
        if qu.conversion_multiplier == conversion_factor and suffix in self.symbol_map:
            return True

        return False

    def construct_map(self):
        # Special classes to handle
        # qudt:DerivedUnit
        # qudt:DecimalPrefixUnit

        for qu in self.rp.get_details():
            if not hasattr(qu, 'conversion_offset'):
                continue

            if hasattr(qu, 'label') and si_prefix.is_si_prefix(qu.label.lower()):
                self.si_prefix_map[qu.symbol] = qu
                self.si_prefix_map[qu.label.lower()] = qu
                continue

            if hasattr(qu, 'symbol'):
                self.symbol_map[qu.symbol] = qu

            if hasattr(qu, 'label'):
                self.label_map[qu.label.lower()] = qu

        # Remove some symbols from symbol map
        # Remove units like km, ms which are si prefix + base symbol
        # Check prefix = k, conversion_multiplier = 1000: matches - so same units so don't process
        for symbol in list(self.symbol_map.keys()):
            if self.is_qudt_unit_with_si_prefix(self.symbol_map[symbol]):  # km, ms, etc
                del self.symbol_map[symbol]

        for label in list(self.label_map.keys()):
            if self.is_qudt_unit_with_si_prefix(self.label_map[label]):
                del self.label_map[label]

        # Custom cases
        if 'kg' in self.symbol_map:
            del self.symbol_map['kg']
        if 'kilogram' in self.label_map:
            del self.label_map['kilogram']

        '''
        # print initial tables to monitor files
        monfile_symb = open("monitor_symb.txt", "w")
        for (keyd,vald) in self.symbol_map.items():
            #monfile_symb.write(str(keyd) + ", " + str(vald) + '\n')
            monfile_symb.write(str(keyd) + ", " + str(vald.label) + '\n')
        monfile_symb.close()

        monfile_lbl = open("monitor_lbl.txt", "w")
        for (keyd,vald) in self.label_map.items():
            #monfile_lbl.write(str(keyd) + ", " + str(vald) + '\n')
            monfile_lbl.write(str(keyd) + ", " + str(vald.label) + '\n')
        monfile_lbl.close()

        monfile_si = open("monitor_si.txt", "w")
        for (keyd,vald) in self.si_prefix_map.items():
            #monfile_si.write(str(keyd) + ", " + str(vald) + '\n')
            monfile_si.write(str(keyd) + ", " + str(vald.label) + '\n')
        monfile_si.close()
        '''
