class Unit:
    def __init__(self, symbol, multiplier, exponent, comment):
        self.symbol = symbol
        self.multiplier = multiplier
        self.exponent = exponent
        self.comment = comment

    def __repr__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    @staticmethod
    def negate_exponent(simpleUnit):  # simpleUnit type Unit
        unit = Unit(simpleUnit.symbol, simpleUnit.multiplier, simpleUnit.exponent, simpleUnit.comment)

        if unit.exponent is None:
            unit.exponent = '-1'
        elif unit.exponent[0] == '-':
            unit.exponent = unit.exponent[1:]
        else:
            unit.exponent = '-' + unit.exponent

        return unit
