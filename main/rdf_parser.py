'''
The RDFParser class is used to parse the qudt unit.owl ontology file
and create instances of QudtUnit from the file.
'''

from .qudt_unit import QudtUnit
from os.path import isfile, join, splitext
from rdflib import Graph, RDF, RDFS, OWL, BNode, URIRef, Namespace

# TTL/OWL files
class RDFParser:
    # QUDT V1
    QUDT = Namespace("http://data.nasa.gov/qudt/owl/qudt#")

    def __init__(self, dir_path, file_name):
        self.g = Graph()
        if splitext(file_name)[1] == ".ttl":
            self.g.parse(join(dir_path, file_name), format='n3')
        elif splitext(file_name)[1] == ".owl":
            self.g.parse(join(dir_path, file_name))

    def get_details(self, rdftype=OWL.Class):
        for s in self.g.subjects():

            # ignore blank nodes; rdflib.term.BNode
            if isinstance(s, BNode):
                continue

            qu = QudtUnit()
            qu.set_uri(s.strip())

            # TODO: add check if there are multiple defintions
            for label in self.g.objects(s, RDFS.label):
                qu.set_label(str(label.split(" (")[0])) # TODO
            for symbol in self.g.objects(s, self.QUDT.symbol):
                qu.set_symbol(str(symbol))
            for abbr in self.g.objects(s, self.QUDT.abbreviation):
                qu.set_abbr(str(abbr))
            ''' TODO: there is more than 1 quantity_kind
                i.e.: unit:Kilocalorie has qudt:quantityKind { quantity:EnergyAndWork, quantity:ThermalEnergy} '''
            for quantity_kind in self.g.objects(s, self.QUDT.quantityKind):
                qu.set_quantity_kind(quantity_kind)
            for conversion_multiplier in self.g.objects(s, self.QUDT.conversionMultiplier):
                qu.set_conversion_multiplier(float(conversion_multiplier))
            for conversion_offset in self.g.objects(s, self.QUDT.conversionOffset):
                qu.set_conversion_offset(float(conversion_offset))

            yield qu
