'''
The UnitVisitor class deals with the construction of
Unit and CompoundUnit instances.
'''

from arpeggio import PTNodeVisitor
from .compound_unit import CompoundUnit
from .unit import Unit

class UnitVisitor(PTNodeVisitor):
    def visit_compound_unit(self, node, children):
        if len(children) == 1:
            return CompoundUnit(children[0], None)
        else:
            return CompoundUnit(children[0], children[1])

    def visit_numerator(self, node, children):
        numerator_list = []
        for child in children:
            if isinstance(child, Unit):
                numerator_list.append(child)

        return numerator_list

    def visit_denominator(self, node, children):
        denominator_list = []
        for child in children:
            if isinstance(child, Unit):
                denominator_list.append(child)

        return denominator_list

    def visit_number(self, node, children):
        if children[0] == '-':
            return '-' + children[1]
        else:
            return children[0]

    def visit_exponent(self, node, children):
        if children[0] == '^':
            return children[1]
        else:
            return children[0]

    #     def visit_comment(self, node, children):
    #         return children[0]

    # TODO: this is similar to visit_number
    def visit_multiplier(self, node, children):
        if children[0] == '-':
            return '-' + children[1]
        else:
            return children[0]

    def visit_simple_unit(self, node, children):
        exponent_multiplier = None
        if children.symbol[0][:2] == 'sq' and len(children.symbol[0]) > 2:
            # handle sq* (i.e. sqm, sqkm, sqft, sqmi)
            children.symbol[0] = children.symbol[0][2:]
            exponent_multiplier = 2
        elif children.symbol[0][:2] == 'cu' and len(children.symbol[0]) > 3:
            # handle cu* (i.e. cuyd, cuft)
            children.symbol[0] = children.symbol[0][2:]
            exponent_multiplier = 3

        try:
            multiplier = children.multiplier[0]
        except:
            multiplier = None

        try:
            exponent = children.exponent[0]
        except:
            exponent = None
        # adjust exponent
        if exponent_multiplier:
            if exponent:
                exponent = str(int(exponent) * exponent_multiplier)
            else:
                exponent = str(exponent_multiplier)

        try:
            comment = children.comment[0]
        except:
            comment = None

        return Unit(children.symbol[0], multiplier, exponent, comment)