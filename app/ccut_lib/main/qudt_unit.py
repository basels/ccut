'''
The QudtUnit class defines a class for any unit of measurement
used in the CCUT service.
'''

from rdflib import URIRef

class QudtUnit:
    def __init__(self):
        pass

    def set_uri(self, uri: URIRef):
        self.uri = uri

    def set_label(self, label: str):
        self.label = label

    def set_symbol(self, symbol: str):
        self.symbol = symbol

    def set_abbr(self, abbr: str):
        self.abbr = abbr

    def set_quantity_kind(self, quantity_kind: URIRef):
        self.quantity_kind = quantity_kind

    def set_conversion_multiplier(self, conversion_multiplier: float):
        self.conversion_multiplier = conversion_multiplier

    def set_conversion_offset(self, conversion_offset: float):
        self.conversion_offset = conversion_offset

    def __repr__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
