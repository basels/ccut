'''
The SymbolMap is a singleton class to be accessed and used by the service.
It holds a map (dictionary) of symbols ('symbol_map'), labels ('label_map')
and SI prefixes ('si_prefix_map').
'''

from json import load
from .config import Config
from .qudt_unit import QudtUnit
from .rdf_parser import RDFParser
from .si_prefix import SIPrefix

INDEX_NAME_URI = 'uri'
INDEX_NAME_QUANTITYKIND = 'quantityKind'
INDEX_NAME_PREFIX = 'prefix'
INDEX_NAME_CONVERSION_MULTIPLIER = 'conversion_multiplier'
INDEX_NAME_CONVERSION_OFFSET = 'conversion_offset'
INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER = 'prefix_conversion_multiplier'
INDEX_NAME_PREFIX_CONVERSION_OFFSET = 'prefix_conversion_offset'

# Use as singleton class
class SymbolMap:

    instance = None

    def __init__(self):

        self.symbol_map = dict()
        self.label_map = dict()
        self.si_prefix_map = dict()

        # load QUDT files
        for ontof in Config.DATA_QUDT_V1_ONTO_FILES:
            self.rp = RDFParser(Config.DATA_DIR, ontof)
        # user-defined-units
        with open(f'{Config.DATA_DIR}/{Config.DATA_USER_DEFINED_UNITS_FILE}', 'r') as read_file:
            self.udu = load(read_file)
        # label extensions for existing instances
        with open(f'{Config.DATA_DIR}/{Config.DATA_LABELS_EXTENSION_MAP_FILE}', 'r') as read_file:
            self.lbl_ex = load(read_file)

        self.init_list_of_predfined_priorities()
        self.construct_map()
        self.add_user_defined_instances()

        del self.rp
        del self.udu
        del self.lbl_ex
        del self.udp

    @staticmethod
    def get_instance() -> 'SymbolMap':
        if SymbolMap.instance is None:
            SymbolMap.instance = SymbolMap()
        return SymbolMap.instance

    def is_qudt_unit_with_si_prefix(self, qu: QudtUnit):
        ''' Return True for km, ms, etc, False for mX '''
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

    def init_list_of_predfined_priorities(self):
        # pre-defined priorities
        with open(f'{Config.DATA_DIR}/{Config.DATA_PRE_DEFINED_PRIO_FILE}', 'r') as read_file:
            glob_udp = load(read_file)
        self.udp = dict()
        for symb_key, symb_opts in glob_udp['instances'].items():
            self.udp[symb_key] = dict()
            for inst_short_uri, inst_prio in symb_opts.items():
                inst_long_uri = inst_short_uri
                ns_prfx_candidate = inst_short_uri.split(':')[0]
                if ns_prfx_candidate in glob_udp['namespaces']:
                    inst_long_uri = glob_udp['namespaces'][ns_prfx_candidate] + ''.join(inst_short_uri.split(':')[1:])
                self.udp[symb_key][inst_long_uri] = inst_prio

    def get_uri_prio(self, symbol, uri):
        if symbol in self.udp:
            if uri in self.udp[symbol]:
                return self.udp[symbol][uri]
        return 1

    def update_symbol_and_labels_maps(self, qu):
        # clean uri string
        qu_str_uri = qu.uri.strip()

        # label map
        llabel = qu.label.lower()
        if hasattr(qu, 'label') and llabel not in self.label_map:
            # TODO: check if there are cases where it already exists in map
            self.label_map[llabel] = qu
        # check if user supplied additional labels
        if qu_str_uri in self.lbl_ex:
            for ex_label in self.lbl_ex[qu_str_uri]:
                if ex_label not in self.label_map:
                    self.label_map[ex_label] = qu
            del self.lbl_ex[qu_str_uri]

        # symbol map
        symb = qu.symbol
        prio = self.get_uri_prio(symb, qu_str_uri)
        if symb not in self.symbol_map:
            # create the first instance in the list
            self.symbol_map[symb] = [(prio, qu)]
            return
        # symbol exists, check if diff uri
        curr_list = self.symbol_map[symb]
        insrt_qidx = 0
        for qinst in curr_list:
            existing_prio = qinst[0]
            existing_uri = qinst[1].uri.strip()
            if qu_str_uri == existing_uri:
                return
            if existing_prio < prio:
                # this index is to determine where we push the new item
                insrt_qidx += 1
        # reached here without finding uri, insert to PQ
        self.symbol_map[symb].insert(insrt_qidx, (prio, qu))

    def add_user_defined_instances(self):
        # check if user provided additional instances (non QUDT)
        for uri, unit_attrs in self.udu.items():
            if 'symbol' in unit_attrs:
                new_symbol = unit_attrs['symbol']
                if new_symbol not in self.symbol_map:
                    n_qu = QudtUnit()
                    n_qu.set_uri(uri)
                    n_qu.set_symbol(new_symbol)
                    n_qu.set_label(unit_attrs['label'])
                    n_qu.set_abbr(unit_attrs['abbr'])
                    n_qu.set_quantity_kind(unit_attrs['quantityKind'])
                    n_qu.set_conversion_multiplier(float(unit_attrs['conversion_multiplier']))
                    n_qu.set_conversion_offset(float(unit_attrs['conversion_offset']))
                    self.update_symbol_and_labels_maps(n_qu)

    def construct_map(self):
        ''' Special classes to handle
                qudt:DerivedUnit
                qudt:DecimalPrefixUnit '''

        for qu in self.rp.get_details():
            # clean uri string of the current qu (QudtUnit) instance
            qu_str_uri = qu.uri.strip()
            
            # check if user has provided additional attributes for this qu
            if qu_str_uri in self.udu and qu.symbol not in self.symbol_map:
                ud_qu = self.udu[qu_str_uri]
                for key, val in ud_qu.items():
                    if not hasattr(qu, key) and key in ud_qu:
                        setattr(qu, key, ud_qu[key])
                del self.udu[qu_str_uri]

            # if qu doesn't have conversion multiplier, skip
            if not hasattr(qu, INDEX_NAME_CONVERSION_MULTIPLIER):
                continue

            # if qu label is si-prefix then add to si_prefix_map and skip
            if hasattr(qu, 'label') and SIPrefix.is_si_prefix(qu.label.lower()):
                self.si_prefix_map[qu.symbol] = qu
                self.si_prefix_map[qu.label.lower()] = qu
                continue

            # if qu has symbol (and conversion multiplier), add to symbol_map
            if hasattr(qu, 'symbol'):
                self.update_symbol_and_labels_maps(qu)

        ''' Remove some symbols from symbol map:
                Remove units like km, ms which are si prefix + base symbol
                Check prefix = k, conversion_multiplier = 1000: matches - so same units so don't process '''
        for symbol in list(self.symbol_map.keys()):
            if self.is_qudt_unit_with_si_prefix(self.symbol_map[symbol][0][1]):  # km, ms, etc
                del self.symbol_map[symbol]

        for label in list(self.label_map.keys()):
            if self.is_qudt_unit_with_si_prefix(self.label_map[label]):
                del self.label_map[label]

        # Custom cases
        if 'kg' in self.symbol_map:
            del self.symbol_map['kg']
        if 'kilogram' in self.label_map:
            del self.label_map['kilogram']
