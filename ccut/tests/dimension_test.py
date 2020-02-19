from ..main.dimension import DimensionVector

def test():
    assert DimensionVector().set_dimensions("M1.1").raise_to_power(2).get_abbr() == 'M2.2'
    assert DimensionVector().set_dimensions("M1.1 L-1.2").raise_to_power(2).get_abbr() == 'M2.2 L-2.4'
    assert DimensionVector().set_dimensions("M").raise_to_power(1).get_abbr() == 'M'
    assert DimensionVector().set_dimensions("M L T").raise_to_power(2).get_abbr() == 'M2 L2 T2'

    assert str((DimensionVector().set_dimensions("M L2 D2") + DimensionVector().set_dimensions(
        "L3 Te-1 D-3")).get_dimension_vector()) == "[M 1.0, L 5.0, T 0, I 0, Te -1.0, N 0, J 0, D -1.0, C 0, B 0]"

    assert str(DimensionVector().set_dimensions(
        "M L2 Te-1").get_dimension_vector()) == "[M 1.0, L 2.0, T 0, I 0, Te -1.0, N 0, J 0, D 0, C 0, B 0]"

    assert DimensionVector().set_dimensions("M").get_abbr() == "M"
    assert DimensionVector().set_dimensions("L2").get_abbr() == "L2"
    assert DimensionVector().set_dimensions("L2 T-2").get_abbr() == "L2 T-2"
    assert DimensionVector().set_dimensions("T-2 L2").get_abbr() == "L2 T-2"
    assert DimensionVector().set_dimensions("T-2.0 L2.1").get_abbr() == "L2.1 T-2"
    assert DimensionVector().set_dimensions("C D J N Te I T L M").get_abbr() == "M L T I Te N J D C"
    assert DimensionVector().set_dimensions("T2.0 L2.1").get_abbr() == "L2.1 T2"
    assert DimensionVector().set_dimensions("Te3 T3").get_abbr() == "T3 Te3"
