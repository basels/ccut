from main.symbol_map import SymbolMap


class UnitMatch:

    def find_best_unit_match_by_string(symbol, unit_map: SymbolMap):
        if symbol in unit_map.symbol_map:
            return {
                'uri': str(unit_map.symbol_map[symbol].uri),
                'quantityKind': str(unit_map.symbol_map[symbol].quantity_kind),
                'prefix': None,
                'conversion_multiplier': unit_map.symbol_map[symbol].conversion_multiplier,
                'conversion_offset': unit_map.symbol_map[symbol].conversion_offset
            }

        if symbol in unit_map.label_map:
            return {
                'uri': str(unit_map.label_map[symbol].uri),
                'quantityKind': str(unit_map.label_map[symbol].quantity_kind),
                'prefix': None,
                'conversion_multiplier': unit_map.label_map[symbol].conversion_multiplier,
                'conversion_offset': unit_map.label_map[symbol].conversion_offset
            }

        for i in range(5): # TODO: why '5'?
            prefix, suffix = symbol[0:i + 1], symbol[i + 1:]
            if prefix in unit_map.si_prefix_map and suffix in unit_map.symbol_map:
                return {
                    'uri': str(unit_map.symbol_map[suffix].uri),
                    'quantityKind': str(unit_map.symbol_map[suffix].quantity_kind),
                    'prefix': str(unit_map.si_prefix_map[prefix].uri),
                    'prefix_conversion_multiplier': unit_map.si_prefix_map[prefix].conversion_multiplier,
                    'prefix_conversion_offset': unit_map.si_prefix_map[prefix].conversion_offset,
                    'conversion_multiplier': unit_map.symbol_map[suffix].conversion_multiplier,
                    'conversion_offset': unit_map.symbol_map[suffix].conversion_offset
                }
            if prefix in unit_map.si_prefix_map and suffix and suffix.lower() in unit_map.label_map:
                return {
                    'uri': str(unit_map.label_map[suffix].uri),
                    'quantityKind': str(unit_map.label_map[suffix].quantity_kind),
                    'prefix': str(unit_map.si_prefix_map[prefix].uri),
                    'prefix_conversion_multiplier': unit_map.si_prefix_map[prefix].conversion_multiplier,
                    'prefix_conversion_offset': unit_map.si_prefix_map[prefix].conversion_offset,
                    'conversion_multiplier': unit_map.label_map[suffix].conversion_multiplier,
                    'conversion_offset': unit_map.label_map[suffix].conversion_offset
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