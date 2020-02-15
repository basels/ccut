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

def get_full_ns_by_prefix(ns_dict, ns_candidate):
    ns_cand_split_lst = ns_candidate.split(':')
    ns_short = ns_cand_split_lst[0]
    if ns_short in ns_dict:
        return ns_dict[ns_short] + ''.join(ns_cand_split_lst[1:])
    return ns_candidate

# Use as singleton class
class SymbolMap:

    instance = None

    def __init__(self):

        print('\033[35m' + '-'*20 + ' Initializing CCUT SymbolMap instance ' + '-'*20 + '\033[0m')
        self.symbol_map = dict()
        self.label_map = dict()
        self.si_prefix_map = dict()

        # load QUDT files
        for ontof in Config.DATA_QUDT_V1_ONTO_FILES:
            self.rp = RDFParser(Config.DATA_DIR, ontof)        
        # label extensions for existing instances
        with open(f'{Config.DATA_DIR}/{Config.DATA_LABELS_EXTENSION_MAP_FILE}', 'r') as read_file:
            self.lbl_ex = load(read_file)

        self.init_list_of_predefined_units()
        self.init_list_of_predfined_priorities()
        self.construct_map()
        self.add_user_defined_instances()
        self.print_duplications_on_symbols()

        del self.rp
        del self.udu
        del self.lbl_ex
        del self.udp
        print('\033[35m' + '-'*15 + ' Finished initializing CCUT SymbolMap instance ' + '-'*16 + '\033[0m')

    @staticmethod
    def get_instance() -> 'SymbolMap':
        if SymbolMap.instance is None:
            SymbolMap.instance = SymbolMap()
        return SymbolMap.instance

    def is_prefix_suffix_of_same_qudt_unit(self, qu: QudtUnit, pre: str, suf: str):
        conversion_factor = SIPrefix.get_factor(pre)
        if conversion_factor and suf in self.symbol_map:
            # get head suffix qu
            squ = self.symbol_map[suf][0][1]
            conversion_ratio = qu.conversion_multiplier/squ.conversion_multiplier
            if conversion_ratio == conversion_factor:
                return True
        return False

    def is_qudt_unit_with_si_prefix(self, qu: QudtUnit):
        ''' Return True for km, ms, etc, False for mX '''
        if not hasattr(qu, INDEX_NAME_CONVERSION_MULTIPLIER) or not hasattr(qu, 'symbol'):
            return False
        prefix, suffix = qu.symbol[0], qu.symbol[1:]
        if self.is_prefix_suffix_of_same_qudt_unit(qu, prefix, suffix):
            return True
        prefix, suffix = qu.symbol[:2], qu.symbol[2:]
        if self.is_prefix_suffix_of_same_qudt_unit(qu, prefix, suffix):
            return True
        return False

    def init_list_of_predfined_priorities(self):
        # pre-defined priorities
        with open(f'{Config.DATA_DIR}/{Config.DATA_PRE_DEFINED_PRIO_FILE}', 'r') as read_file:
            glob_dict = load(read_file)
        self.udp = dict()
        for symb_key, symb_opts in glob_dict['instances'].items():
            self.udp[symb_key] = dict()
            for inst_short_uri, inst_prio in symb_opts.items():
                inst_long_uri = get_full_ns_by_prefix(glob_dict['namespaces'], inst_short_uri)
                self.udp[symb_key][inst_long_uri] = inst_prio

    def init_list_of_predefined_units(self):
        # pre-defined units
        with open(f'{Config.DATA_DIR}/{Config.DATA_USER_DEFINED_UNITS_FILE}', 'r') as read_file:
            glob_dict = load(read_file)
        self.udu = dict()
        for inst_key, inst_values in glob_dict['instances'].items():
            inst_full_key = get_full_ns_by_prefix(glob_dict['namespaces'], inst_key)
            self.udu[inst_full_key] = inst_values

    def get_uri_prio(self, symbol, uri):
        if symbol in self.udp:
            if uri in self.udp[symbol]:
                return self.udp[symbol][uri]

        if symbol in self.symbol_map:
            return self.symbol_map[symbol][-1][0] + 1

        return 1

    def print_duplications_on_symbols(self):
        for symb_key, symb_list_of_prio_inst_tup in self.symbol_map.items():
            num_of_instances_in_symbol = len(symb_list_of_prio_inst_tup)
            if num_of_instances_in_symbol > 1:
                print(f'\033[93m "{symb_key}" has {num_of_instances_in_symbol} instances\033[0m')
                for prio, inst in symb_list_of_prio_inst_tup:
                    print(f'   [{prio}] {inst.uri}')

    def update_symbol_and_labels_maps(self, qu):
        # label map
        if hasattr(qu, 'label'):
            llabel = qu.label.lower()
            if llabel not in self.label_map:
                self.label_map[llabel] = qu
        # check if user supplied additional labels
        if qu.uri in self.lbl_ex:
            for ex_label in self.lbl_ex[qu.uri]:
                if ex_label not in self.label_map:
                    self.label_map[ex_label] = qu
                elif qu.uri != self.label_map[ex_label].uri:
                    print(f'\033[91m "{ex_label} | {qu.uri}" has already been defined ({self.label_map[ex_label].uri})\033[0m')
            del self.lbl_ex[qu.uri]

        # symbol map
        symb = qu.symbol
        prio = self.get_uri_prio(symb, qu.uri)
        if symb not in self.symbol_map:
            # create the first instance in the list
            self.symbol_map[symb] = [(prio, qu)]
            return
        # symbol exists, check if diff uri
        curr_list = self.symbol_map[symb]
        insrt_qidx = 0
        for qinst in curr_list:
            existing_prio = qinst[0]
            existing_uri = qinst[1].uri
            if qu.uri == existing_uri:
                return
            if existing_prio < prio:
                # this index is to determine where we push the new item
                insrt_qidx += 1
        # reached here without finding uri, insert to PQ
        self.symbol_map[symb].insert(insrt_qidx, (prio, qu))

    def add_user_defined_instances(self):
        # check if user provided additional instances (non QUDT)
        for uri, unit_attrs in self.udu.items():
            if 'symbol' in unit_attrs and \
                INDEX_NAME_CONVERSION_MULTIPLIER in unit_attrs:
                n_qu = QudtUnit()
                n_qu.set_uri(uri)
                n_qu.set_symbol(unit_attrs['symbol'])
                n_qu.set_label(unit_attrs['label'])
                n_qu.set_abbr(unit_attrs['abbr'])
                n_qu.set_quantity_kind(unit_attrs[INDEX_NAME_QUANTITYKIND])
                n_qu.set_conversion_multiplier(float(unit_attrs[INDEX_NAME_CONVERSION_MULTIPLIER]))
                n_qu.set_conversion_offset(float(unit_attrs[INDEX_NAME_CONVERSION_OFFSET]))
                self.update_symbol_and_labels_maps(n_qu)

    def construct_map(self):
        ''' Special classes to handle
                qudt:DerivedUnit
                qudt:DecimalPrefixUnit '''

        for qu in self.rp.get_details():
            # check if user has provided additional attributes for this qu
            if qu.uri in self.udu:
                ud_qu = self.udu[qu.uri]
                if 'symbol' in ud_qu:
                    qu.symbol = ud_qu['symbol']
                if qu.symbol not in self.symbol_map:
                    for key, val in ud_qu.items():
                        if not hasattr(qu, key) and key in ud_qu:
                            setattr(qu, key, ud_qu[key])
                    del self.udu[qu.uri]

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
