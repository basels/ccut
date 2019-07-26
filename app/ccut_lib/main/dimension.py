'''
The Dimension and DimensionVector classes are used to capture and
allow the construction of a proper dimensional representation of compound units.
'''

from re import search, IGNORECASE

class Dimension:
    def __init__(self, symbol, uri, exponent: float):  # L, Length, -1
        self.symbol = symbol
        self.uri = uri
        self.exponent = exponent

    def __repr__(self):
        return self.symbol + " " + str(self.exponent)

class DimensionVector:
    def __init__(self):
        self.dimension_vector = self.get_empty_dimension_vector()

    def __add__(self, new):
        ret = DimensionVector()
        for i, (left, right) in enumerate(zip(self.dimension_vector, new.dimension_vector)):
            ret.dimension_vector[i].exponent = left.exponent + right.exponent

        return ret

    def raise_to_power(self, exponent):
        exponent = float(exponent)
        for dimension in self.dimension_vector:
            dimension.exponent *= exponent

        return self

    def set_dimensions(self, dimension_string):
        dimensions = dimension_string.split(" ")

        dim_map = dict()
        # Create a dimension map
        for dimension in dimensions:
            try:
                exponent = float(search("-?[0-9]+\.[0-9]+|-?[0-9]+", dimension).group(0))
            except:
                exponent = 1.0

            symbol = search("[a-z]+", dimension, flags=IGNORECASE).group(0)

            dim_map[symbol] = exponent

        for dimension in self.dimension_vector:
            if dimension.symbol in dim_map:
                dimension.exponent = dim_map[dimension.symbol]

        return self

    def get_dimension_vector(self):
        return self.dimension_vector

    def get_abbr(self):
        abbr = ""
        for dimension in self.dimension_vector:
            if dimension.exponent != 0:
                abbr += dimension.symbol

                if dimension.exponent == 1:
                    pass
                elif float(dimension.exponent).is_integer():
                    abbr += str(int(dimension.exponent))
                else:
                    abbr += str(dimension.exponent)

                abbr += " "

        return abbr.strip()

    def get_empty_dimension_vector(self):
        dimensionVector = []

        # TODO: add URIs and use a better representation
        dimensionVector.append(Dimension('M', None, 0))
        dimensionVector.append(Dimension('L', None, 0))
        dimensionVector.append(Dimension('T', None, 0))
        dimensionVector.append(Dimension('I', None, 0))
        dimensionVector.append(Dimension('Te', None, 0))
        dimensionVector.append(Dimension('N', None, 0))
        dimensionVector.append(Dimension('J', None, 0))
        dimensionVector.append(Dimension('D', None, 0))
        dimensionVector.append(Dimension('C', None, 0))
        dimensionVector.append(Dimension('B', None, 0))

        return dimensionVector

