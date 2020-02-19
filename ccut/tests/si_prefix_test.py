from ..main.si_prefix import SIPrefix

def test():
    assert SIPrefix.is_si_prefix("m")
    assert SIPrefix.is_si_prefix("f")
    assert SIPrefix.is_si_prefix("milli")
    assert SIPrefix.is_si_prefix("Milli")
    assert SIPrefix.is_si_prefix("Y")
    assert SIPrefix.is_si_prefix("K") == False
    assert SIPrefix.is_si_prefix("X") == False
    assert SIPrefix.is_si_prefix("A") == False
    assert SIPrefix.is_si_prefix("Ax") == False

    assert SIPrefix.get_factor("m") == 1e-3
    assert SIPrefix.get_factor("Milli") == 1e-3
