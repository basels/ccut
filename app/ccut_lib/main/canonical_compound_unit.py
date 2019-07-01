'''
The CanonicalCompoundUnit class wraps the CompoundUnit class
and binds it to a dimension.
'''

from .canonical_simple_unit import CanonicalSimpleUnit, QUDT_PROPERTIES_NAMESPACE, CCUT_NAMESPACE
from .compound_unit import CompoundUnit
from .dimension import DimensionVector
from .symbol_map import SymbolMap
from .unit import Unit
from .unit_match import UnitMatch
from typing import *

class CanonicalCompoundUnit:
    def __init__(self, compoundUnit: CompoundUnit):
        self.unit_obj = dict()
        self.symbol_map_instance = SymbolMap.get_instance()

        dimensionVector = DimensionVector()

        # Rearrange numerator and denominator
        # compoundUnit = self.rearrange_numerator_denominator(compoundUnit)
        compoundUnit = self.merge_same_units(compoundUnit)
        self.unit_obj[f'{QUDT_PROPERTIES_NAMESPACE}:abbreviation'] = self.get_abbreviation(compoundUnit)

        # Map compound unit to any known quantities
        qudtAbbr = self.get_abbreviation(compoundUnit, qudtStyle=True)
        compoundUnitQuantity = UnitMatch.find_best_unit_match(qudtAbbr, self.symbol_map_instance)
        if compoundUnitQuantity is not None:
            pass

        self.unit_obj[f'{CCUT_NAMESPACE}:hasPart'] = []

        if compoundUnit.numerator:
            for n in compoundUnit.numerator:
                csu = CanonicalSimpleUnit(n).get_unit_object()
                self.unit_obj[f'{CCUT_NAMESPACE}:hasPart'].append(csu)
                dimensionVector += DimensionVector().set_dimensions(csu[f'{CCUT_NAMESPACE}:hasDimension']).raise_to_power(
                    n.exponent or 1)

        if compoundUnit.denominator:
            for d in compoundUnit.denominator:
                csu = CanonicalSimpleUnit(Unit.negate_exponent(d)).get_unit_object()
                self.unit_obj[f'{CCUT_NAMESPACE}:hasPart'].append(csu)
                # This is line is too complicated. Must be simplified
                dimensionVector += DimensionVector().set_dimensions(csu[f'{CCUT_NAMESPACE}:hasDimension']).raise_to_power(
                    Unit.negate_exponent(d).exponent or 1)

                # Calculate dimension of unit
        self.unit_obj[f'{CCUT_NAMESPACE}:hasDimension'] = dimensionVector.get_abbr()

    def merge_same_units(self, compoundUnit: CompoundUnit):
        cu = CompoundUnit([], [])

        if compoundUnit.numerator:
            cu.numerator = self.merge_list(compoundUnit.numerator)
        if compoundUnit.denominator:
            cu.denominator = self.merge_list(compoundUnit.denominator)

        return cu

    def merge_list(self, l: List[Unit]):
        merged_list = []

        # Rule for merging:
        # multiplier should be None for all
        # exponent will be added. None = 1
        for i in range(len(l)):
            if i == 0:
                merged_list.append(l[i])
            else:
                r_unit = l[i]
                merge_success = False
                for j in range(len(merged_list)):
                    l_unit = merged_list[j]
                    try:
                        merged_unit = self.merge_units(l_unit, r_unit)
                        merged_list[j] = merged_unit
                        merge_success = True
                        break
                    except Exception as e:
                        pass

                if not merge_success:
                    merged_list.append(r_unit)

        return merged_list

    def merge_units(self, l_unit: Unit, r_unit: Unit):
        if l_unit.multiplier is not None or r_unit.multiplier is not None:
            raise Exception("cannot merge")

        if l_unit.symbol != r_unit.symbol:
            raise Exception("cannot merge")

        e1 = l_unit.exponent or 1
        e2 = r_unit.exponent or 1

        new_e = str(int(e1) + int(e2))

        new_unit = Unit(l_unit.symbol, None, new_e, l_unit.comment or r_unit.comment)
        return new_unit

    def get_unit_object(self):
        return self.unit_obj

    def get_abbreviation(self, compoundUnit, qudtStyle=False):
        abbr = []
        for n in compoundUnit.numerator:
            abbr.append(self.get_simple_unit_abbr(n, qudtStyle))
        if compoundUnit.denominator is not None:
            for d in compoundUnit.denominator:
                abbr.append(self.get_simple_unit_abbr(Unit.negate_exponent(d), qudtStyle))

        return " ".join(abbr)

    def get_simple_unit_abbr(self, unit, qudtStyle=False):
        abbr = ""
        if unit.multiplier is not None:
            abbr += unit.multiplier
        abbr += unit.symbol
        if unit.exponent is not None:
            if qudtStyle:
                abbr += "^"
            abbr += unit.exponent

        return abbr
