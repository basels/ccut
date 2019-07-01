'''
The UnitMatch class is used to find the best unit match for a given string.
'''

from main.symbol_map import SymbolMap, INDEX_NAME_URI, INDEX_NAME_QUANTITYKIND, INDEX_NAME_PREFIX, \
                            INDEX_NAME_CONVERSION_MULTIPLIER, INDEX_NAME_CONVERSION_OFFSET, \
                            INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER, INDEX_NAME_PREFIX_CONVERSION_OFFSET

class UnitMatch:

    def find_best_unit_match_by_string(symbol, unit_map: SymbolMap):
        if symbol in unit_map.symbol_map:
            return {
                INDEX_NAME_URI: str(unit_map.symbol_map[symbol].uri),
                INDEX_NAME_QUANTITYKIND: str(unit_map.symbol_map[symbol].quantity_kind),
                INDEX_NAME_PREFIX: None,
                INDEX_NAME_CONVERSION_MULTIPLIER: unit_map.symbol_map[symbol].conversion_multiplier,
                INDEX_NAME_CONVERSION_OFFSET: unit_map.symbol_map[symbol].conversion_offset
            }

        if symbol in unit_map.label_map:
            return {
                INDEX_NAME_URI: str(unit_map.label_map[symbol].uri),
                INDEX_NAME_QUANTITYKIND: str(unit_map.label_map[symbol].quantity_kind),
                INDEX_NAME_PREFIX: None,
                INDEX_NAME_CONVERSION_MULTIPLIER: unit_map.label_map[symbol].conversion_multiplier,
                INDEX_NAME_CONVERSION_OFFSET: unit_map.label_map[symbol].conversion_offset
            }

        for i in range(5): # longest prefix is 5 chars long
            prefix, suffix = symbol[0:i + 1], symbol[i + 1:]
            if prefix in unit_map.si_prefix_map and suffix in unit_map.symbol_map:
                return {
                    INDEX_NAME_URI: str(unit_map.symbol_map[suffix].uri),
                    INDEX_NAME_QUANTITYKIND: str(unit_map.symbol_map[suffix].quantity_kind),
                    INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                    INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                    INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                    INDEX_NAME_CONVERSION_MULTIPLIER: unit_map.symbol_map[suffix].conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: unit_map.symbol_map[suffix].conversion_offset
                }
            if prefix in unit_map.si_prefix_map and suffix and suffix.lower() in unit_map.label_map:
                return {
                    INDEX_NAME_URI: str(unit_map.label_map[suffix].uri),
                    INDEX_NAME_QUANTITYKIND: str(unit_map.label_map[suffix].quantity_kind),
                    INDEX_NAME_PREFIX: str(unit_map.si_prefix_map[prefix].uri),
                    INDEX_NAME_PREFIX_CONVERSION_MULTIPLIER: unit_map.si_prefix_map[prefix].conversion_multiplier,
                    INDEX_NAME_PREFIX_CONVERSION_OFFSET: unit_map.si_prefix_map[prefix].conversion_offset,
                    INDEX_NAME_CONVERSION_MULTIPLIER: unit_map.label_map[suffix].conversion_multiplier,
                    INDEX_NAME_CONVERSION_OFFSET: unit_map.label_map[suffix].conversion_offset
                }

        return None

    @staticmethod
    def find_best_unit_match(symbol, unit_map):
        # TODO: Full case-insensitive matching
        tmp_symb_str = symbol
        tmp_res = UnitMatch.find_best_unit_match_by_string(tmp_symb_str, unit_map)
        if None == tmp_res:
            tmp_symb_str = symbol.lower()
            tmp_res =  UnitMatch.find_best_unit_match_by_string(tmp_symb_str, unit_map)
        return tmp_res
