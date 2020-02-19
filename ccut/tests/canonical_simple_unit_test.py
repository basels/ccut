from ..main.canonical_simple_unit import CanonicalSimpleUnit
from ..main.unit import Unit

def test():
    u = Unit('kg', None, None, None)
    assert CanonicalSimpleUnit(u).get_unit_object() == {'qudtp:symbol': 'kg',
     'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Gram',
     'ccut:prefix': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Kilo',
     'ccut:hasDimension': 'M',
     'ccut:prefixConversionMultiplier': 1000,
     'ccut:prefixConversionOffset': 0,
     'qudtp:conversionMultiplier': 0.001,
     'qudtp:conversionOffset': 0}

    u = Unit('X', None, None, None)
    assert CanonicalSimpleUnit(u).get_unit_object() == {'qudtp:symbol': 'X',
     'qudtp:quantityKind': 'UNKNOWN TYPE',
     'ccut:hasDimension': 'UNKNOWN DIMENSION',
     'qudtp:conversionMultiplier': None,
     'qudtp:conversionOffset': None}

