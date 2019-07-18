'''
The UnitMatch class is used to find the best unit match for a given string.
'''

from .symbol_map import SymbolMap, INDEX_NAME_URI, INDEX_NAME_QUANTITYKIND, INDEX_NAME_PREFIX, \
                            INDEX_NAME_CONVERSION_MULTIPLIER, INDEX_NAME_CONVERSION_OFFSET, \
                            INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER, INDEX_NAME_PREFIX_CONVERSION_OFFSET

class UnitMatch:

    def find_best_unit_match_by_string(symbol, unit_map: SymbolMap):
        if symbol in unit_map.symbol_map:
            head_qu = unit_map.symbol_map[symbol][0][1] # qu with minimal prio
            return {
                INDEX_NAME_URI: str(head_qu.uri),
                INDEX_NAME_QUANTITYKIND: str(head_qu.quantity_kind),
                INDEX_NAME_PREFIX: None,
                INDEX_NAME_CONVERSION_MULTIPLIER: head_qu.conversion_multiplier,
                INDEX_NAME_CONVERSION_OFFSET: head_qu.conversion_offset
            }

        if symbol in unit_map.label_map:
            lbl_qu = unit_map.label_map[symbol]
            return {
                INDEX_NAME_URI: str(lbl_qu.uri),
                INDEX_NAME_QUANTITYKIND: str(lbl_qu.quantity_kind),
                INDEX_NAME_PREFIX: None,
                INDEX_NAME_CONVERSION_MULTIPLIER: lbl_qu.conversion_multiplier,
                INDEX_NAME_CONVERSION_OFFSET: lbl_qu.conversion_offset
            }

        for i in range(5): # longest prefix is 5 chars long
            prefix, suffix = symbol[0:i + 1], symbol[i + 1:]
            if prefix in unit_map.si_prefix_map and suffix in unit_map.symbol_map:
                head_qu = unit_map.symbol_map[suffix][0][1] # qu with minimal prio
                return {
                    INDEX_NAME_URI: str(head_qu.uri),
                    INDEX_NAME_QUANTITYKIND: str(head_qu.quantity_kind),
                    INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                    INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                    INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                    INDEX_NAME_CONVERSION_MULTIPLIER: head_qu.conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: head_qu.conversion_offset
                }
            if prefix in unit_map.si_prefix_map and suffix and suffix.lower() in unit_map.label_map:
                lbl_qu = unit_map.label_map[suffix]
                return {
                    INDEX_NAME_URI: str(lbl_qu.uri),
                    INDEX_NAME_QUANTITYKIND: str(lbl_qu.quantity_kind),
                    INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                    INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                    INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                    INDEX_NAME_CONVERSION_MULTIPLIER: lbl_qu.conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: lbl_qu.conversion_offset
                }

        return None

    @staticmethod
    def find_best_unit_match(symbol, unit_map):
        tmp_symb_str = symbol
        tmp_res = UnitMatch.find_best_unit_match_by_string(tmp_symb_str, unit_map)
        if None == tmp_res:
            tmp_symb_str = symbol.lower()
            tmp_res =  UnitMatch.find_best_unit_match_by_string(tmp_symb_str, unit_map)
        return tmp_res
