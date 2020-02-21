'''
The UnitMatch class is used to find the best unit match for a given string.
'''

from .symbol_map import SymbolMap, INDEX_NAME_URI, INDEX_NAME_QUANTITYKIND, INDEX_NAME_PREFIX, \
                            INDEX_NAME_CONVERSION_MULTIPLIER, INDEX_NAME_CONVERSION_OFFSET, \
                            INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER, INDEX_NAME_PREFIX_CONVERSION_OFFSET

class UnitMatch:

    def check_if_uri_in_list_of_dictionaries(list_of_dicts, uri):
        for dict_i in list_of_dicts:
            if INDEX_NAME_URI in dict_i and uri == dict_i[INDEX_NAME_URI]:
                return True
        return False

    def find_best_unit_matches_by_string(symbol, unit_map: SymbolMap):
        ''' Find all possible (atomic with optional prefix) unit instances
            that may match a given string symbol from a given symbol map. '''

        lst_of_unit_opts = list() # list of dictionaries, each is an optional match

        if symbol in unit_map.symbol_map:
            for op_qu in unit_map.symbol_map[symbol]:
                qu_inst = op_qu[1] # each op_qu is a tuple of (prio, qu)
                lst_of_unit_opts.append( {
                    INDEX_NAME_URI: str(qu_inst.uri),
                    INDEX_NAME_QUANTITYKIND: str(qu_inst.quantity_kind),
                    INDEX_NAME_PREFIX: None,
                    INDEX_NAME_CONVERSION_MULTIPLIER: qu_inst.conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: qu_inst.conversion_offset })

        if symbol in unit_map.label_map:
            lbl_qu = unit_map.label_map[symbol]
            # check if not already in list of options
            if not UnitMatch.check_if_uri_in_list_of_dictionaries(lst_of_unit_opts, lbl_qu.uri):
                lst_of_unit_opts.append( {
                    INDEX_NAME_URI: str(lbl_qu.uri),
                    INDEX_NAME_QUANTITYKIND: str(lbl_qu.quantity_kind),
                    INDEX_NAME_PREFIX: None,
                    INDEX_NAME_CONVERSION_MULTIPLIER: lbl_qu.conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: lbl_qu.conversion_offset })

        for i in range(5): # longest prefix is 5 chars long
            prefix, suffix = symbol[0:i + 1], symbol[i + 1:]
            if prefix in unit_map.si_prefix_map and suffix in unit_map.symbol_map:
                for op_qu in unit_map.symbol_map[suffix]:
                    qu_inst = op_qu[1] # each op_qu is a tuple of (prio, qu)
                    lst_of_unit_opts.append( {
                        INDEX_NAME_URI: str(qu_inst.uri),
                        INDEX_NAME_QUANTITYKIND: str(qu_inst.quantity_kind),
                        INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                        INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                        INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                        INDEX_NAME_CONVERSION_MULTIPLIER: qu_inst.conversion_multiplier,
                        INDEX_NAME_CONVERSION_OFFSET: qu_inst.conversion_offset})

            if prefix in unit_map.si_prefix_map and suffix and suffix.lower() in unit_map.label_map:
                lbl_qu = unit_map.label_map[suffix]

                # check if not already in list of options
                if not UnitMatch.check_if_uri_in_list_of_dictionaries(lst_of_unit_opts, lbl_qu.uri):
                    lst_of_unit_opts.append( {
                        INDEX_NAME_URI: str(lbl_qu.uri),
                        INDEX_NAME_QUANTITYKIND: str(lbl_qu.quantity_kind),
                        INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                        INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                        INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                        INDEX_NAME_CONVERSION_MULTIPLIER: lbl_qu.conversion_multiplier,
                        INDEX_NAME_CONVERSION_OFFSET: lbl_qu.conversion_offset })

        return lst_of_unit_opts

    @staticmethod
    def find_best_unit_match(symbol, unit_map):
        tmp_symb_str = symbol
        tmp_list_of_unit_options = UnitMatch.find_best_unit_matches_by_string(tmp_symb_str, unit_map)
        if 0 == len(tmp_list_of_unit_options):
            tmp_symb_str = symbol.lower()
            tmp_list_of_unit_options = UnitMatch.find_best_unit_matches_by_string(tmp_symb_str, unit_map)
        if 0 == len(tmp_list_of_unit_options):
            return None
        return tmp_list_of_unit_options
