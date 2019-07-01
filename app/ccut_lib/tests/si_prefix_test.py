from main.si_prefix.SIPrefix import is_si_prefix

def test():
    assert is_si_prefix("m")
    assert is_si_prefix("f")
    assert is_si_prefix("milli")
    assert is_si_prefix("Milli")
    assert is_si_prefix("Y")
    assert is_si_prefix("K") == False
    assert is_si_prefix("X") == False
    assert is_si_prefix("A") == False
    assert is_si_prefix("Ax") == False

    assert get_factor("m") == 1e-3
    assert get_factor("Milli") == 1e-3
