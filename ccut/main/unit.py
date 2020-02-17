'''
The Unit class defines a class for atomic unit of measurement.
It has symbol, multiplier, exponent and comment attributes.
'''

from .currency_symbols import CurrencySymbols

class Unit:
    def __init__(self, symbol, multiplier, exponent, comment):
        # check if currency symbol
        csa = CurrencySymbols.get_symbol(symbol)
        if csa:
            self.symbol = csa
        else:
            self.symbol = symbol
        self.multiplier = multiplier
        self.exponent = exponent
        self.comment = comment

    def __repr__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    @staticmethod
    def negate_exponent(simpleUnit):
        unit = Unit(simpleUnit.symbol, simpleUnit.multiplier, simpleUnit.exponent, simpleUnit.comment)

        if unit.exponent is None:
            unit.exponent = '-1'
        elif unit.exponent[0] == '-':
            unit.exponent = unit.exponent[1:]
        else:
            unit.exponent = '-' + unit.exponent

        return unit