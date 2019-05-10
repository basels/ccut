from main.si_prefix import si_prefix

def test():
    assert si_prefix.is_si_prefix("m")
    assert si_prefix.is_si_prefix("f")
    assert si_prefix.is_si_prefix("milli")
    assert si_prefix.is_si_prefix("Milli")
    assert si_prefix.is_si_prefix("Y")
    assert si_prefix.is_si_prefix("K") == False
    assert si_prefix.is_si_prefix("X") == False
    assert si_prefix.is_si_prefix("A") == False
    assert si_prefix.is_si_prefix("Ax") == False

    assert si_prefix.get_factor("m") == 1e-3
    assert si_prefix.get_factor("Milli") == 1e-3
