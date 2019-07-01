'''
The UnitParser class uses arpeggio to define the grammer of
how to read a language of compound and atomic units.
'''

from arpeggio import RegExMatch as _, Optional, ZeroOrMore, EOF, ParserPython
from .currency_symbols import CurrencySymbols

# "kg/m/s^2"
# "g/cm/s^2"

def symbol(): return ["deg C", _(r'[a-zA-Z]+'), list(CurrencySymbols.currency_symbols.keys())]  # Matches ab, Cd, EF, g, $

def number(): return Optional("-"), _(r'\d*\.\d+|\d+\/\d+|\d+')  # Matches 1.2, .2, 12, 1/2, -1, -1/2 #Does not match 1.2/3, 1.

def multiplier(): return number

def exponent(): return Optional("^"), ([number, ("(", number, ")")])

def comment(): return "[", _(r'[^\]]*'), "]"  # Matches: [soil] [], [123]

def simple_unit(): return Optional(multiplier), symbol, Optional(exponent), Optional(comment)

def numerator(): return simple_unit, ZeroOrMore(Optional([" ", "."]), simple_unit)

def denominator(): return simple_unit, ZeroOrMore(Optional([" ", ".", "/"]), simple_unit)

def compound_unit(): return numerator, Optional("/", denominator), EOF

class UnitParser:
    def __init__(self):
        self.parser = ParserPython(compound_unit)

    def get_parser(self):
        return self.parser