from ..main.symbol_map import SymbolMap

def test():
    s = SymbolMap.get_instance()

    assert 'fm' not in s.symbol_map
    assert 'km' not in s.symbol_map
    assert 'MHz' not in s.symbol_map
    assert 'ms' not in s.symbol_map
    assert 'kg' not in s.symbol_map

    assert 'millisecond' not in s.label_map

    assert 's' in s.symbol_map
    assert 'degC' in s.symbol_map
    assert 'day' in s.label_map
    assert 'meter' in s.label_map

    assert 'k' in s.si_prefix_map

