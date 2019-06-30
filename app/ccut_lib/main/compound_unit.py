'''
The CompoundUnit class defines a class for a compound unit of measurement.
It is composed from two or more atomic units enclosed in a numerator and a denominator.
'''

from typing import List
from main.unit import Unit

class CompoundUnit:
    def __init__(self, numerator: List[Unit], denominator: List[Unit]):
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        return str(self.numerator) + " | " + str(self.denominator)
