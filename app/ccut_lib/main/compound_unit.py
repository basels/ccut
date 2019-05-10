from typing import List
from main.unit import Unit

class CompoundUnit:
    def __init__(self, numerator: List[Unit], denominator: List[Unit]):
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        return str(self.numerator) + " | " + str(self.denominator)
