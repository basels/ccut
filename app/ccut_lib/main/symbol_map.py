'''
The SymbolMap is a singleton class to be accessed and used by the service.
It holds a map (dictionary) of symbols ('symbol_map'), labels ('label_map')
and SI prefixes ('si_prefix_map').
'''

from main.rdf_parser import RDFParser
from main.si_prefix import SIPrefix
from main.qudt_unit import QudtUnit
from main.config import Config
from json import load

INDEX_NAME_URI = 'uri'
INDEX_NAME_QUANTITYKIND = 'quantityKind'
INDEX_NAME_PREFIX = 'prefix'
INDEX_NAME_CONVERSION_MULTIPLIER = 'conversion_multiplier'
INDEX_NAME_CONVERSION_OFFSET = 'conversion_offset'
INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER = 'prefix_conversion_multiplier'
INDEX_NAME_PREFIX_CONVERSION_OFFSET = 'prefix_conversion_offset'

# TODO: remove
DEBUG_WRITE_FILE_HNDLR = open('/Users/baselshbita/repos/ccut/app/ccut_lib/DEBUG_FILE.csv', 'w', encoding='utf-8') 
PRINT_KEYS = ['uri', 'symbol', 'abbr', 'label', 'quantity_kind', 'conversion_multiplier', 'conversion_offset']

def print_to_debug_file(dict_to_print):
    for keyd, vald in dict_to_print.items():
        DEBUG_WRITE_FILE_HNDLR.write(keyd + ',')
        for print_key in PRINT_KEYS:
            val_to_print = ''
            if hasattr(vald, print_key):
                val_to_print = str(getattr(vald, print_key)).strip()
            DEBUG_WRITE_FILE_HNDLR.write(str(val_to_print + ','))
        DEBUG_WRITE_FILE_HNDLR.write('\n')

# Use as singleton class
class SymbolMap:

    instance = None

    def __init__(self):
        self.symbol_map = dict()
        self.label_map = dict()
        self.si_prefix_map = dict()

        for ontof in Config.DATA_QUDT_V1_ONTO_FILES:
            self.rp = RDFParser(Config.DATA_DIR, ontof)

        # user-defined-units list
        self.udu = list()
        with open(f'{Config.DATA_DIR}/{Config.DATA_USER_DEFINED_UNITS_FILE}', 'r') as read_file:
            self.udu = load(read_file)

        # label extensions for existing instances
        with open(f'{Config.DATA_DIR}/{Config.DATA_LABELS_EXTENSION_MAP_FILE}', 'r') as read_file:
            self.lbl_ex = load(read_file)

        self.construct_map()
        del self.rp
        del self.udu
        del self.lbl_ex

    @staticmethod
    def get_instance() -> 'SymbolMap':
        if SymbolMap.instance is None:
            SymbolMap.instance = SymbolMap()

        return SymbolMap.instance

    def is_qudt_unit_with_si_prefix(self, qu: QudtUnit):
        # Return true for km, ms, etc
        # False for mX
        if not hasattr(qu, INDEX_NAME_CONVERSION_MULTIPLIER) or not hasattr(qu, 'symbol'):
            return False

        prefix, suffix = qu.symbol[0], qu.symbol[1:]
        conversion_factor = SIPrefix.get_factor(prefix)
        if qu.conversion_multiplier == conversion_factor and suffix in self.symbol_map:
            return True

        prefix, suffix = qu.symbol[:2], qu.symbol[2:]
        conversion_factor = SIPrefix.get_factor(prefix)
        if qu.conversion_multiplier == conversion_factor and suffix in self.symbol_map:
            return True

        return False

    def construct_map(self):
        # Special classes to handle
        # qudt:DerivedUnit
        # qudt:DecimalPrefixUnit

        for qu in self.rp.get_details():

            qu_str_uri = qu.uri.strip()

            '''
            # TODO: solve duplications
            if hasattr(qu, 'symbol') and qu.symbol in self.symbol_map:
                existing_uri = self.symbol_map[qu.symbol].uri.strip()
                if qu_str_uri != existing_uri:
                    print(f'symbol already defined: {qu.symbol} --> {existing_uri} / {qu_str_uri}')
            '''

            if qu_str_uri in self.udu and qu.symbol not in self.symbol_map:
                ud_qu = self.udu[qu_str_uri]
                for key, val in ud_qu.items():
                    if not hasattr(qu, key) and key in ud_qu:
                        setattr(qu, key, ud_qu[key])

            if not hasattr(qu, INDEX_NAME_CONVERSION_MULTIPLIER):
                continue

            if hasattr(qu, 'label') and SIPrefix.is_si_prefix(qu.label.lower()):
                self.si_prefix_map[qu.symbol] = qu
                self.si_prefix_map[qu.label.lower()] = qu
                continue

            if hasattr(qu, 'symbol'):
                self.symbol_map[qu.symbol] = qu
                # check if user supplied additional labels
                if qu_str_uri in self.lbl_ex:
                    lbls_lst = self.lbl_ex[qu_str_uri]
                    for ex_label in lbls_lst:
                        if ex_label not in self.label_map:
                            self.label_map[ex_label] = qu

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

        # debug
        DEBUG_WRITE_FILE_HNDLR.write('index,')
        for print_key in PRINT_KEYS:
            DEBUG_WRITE_FILE_HNDLR.write(print_key + ',')
        DEBUG_WRITE_FILE_HNDLR.write('\n')
        print_to_debug_file(self.symbol_map)
        print_to_debug_file(self.label_map)
        print_to_debug_file(self.si_prefix_map)

