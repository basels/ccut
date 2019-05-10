import rdflib
from rdflib import RDF, RDFS, OWL, BNode, URIRef, Namespace
from os.path import isfile, join, splitext
from main.qudt_unit import QudtUnit

class rdf_parser:  # TTL/OWL files
    QUDT = Namespace("http://data.nasa.gov/qudt/owl/qudt#") # QUDT V1
    
    # QUDT V2 uses:
    # - Namespace("http://qudt.org/schema/qudt/") 
    # - self.QUDT.hasQuantityKind instead of self.QUDT.quantityKind


    def __init__(self, dir_path, file_name):
        self.g = rdflib.Graph()
        if splitext(file_name)[1] == ".ttl":
            self.g.parse(join(dir_path, file_name), format='n3')
        elif splitext(file_name)[1] == ".owl":
            self.g.parse(join(dir_path, file_name))

    def get_details(self, rdftype=OWL.Class):
        for s in self.g.subjects():
            # Ignore blank nodes; rdflib.term.BNode
            if isinstance(s, BNode):
                continue

            qu = QudtUnit()
            qu.set_uri(s)

            for label in self.g.objects(s, RDFS.label):
                qu.set_label(str(label.split(" (")[0])) # TODO
            for symbol in self.g.objects(s, self.QUDT.symbol):
                qu.set_symbol(str(symbol))
            for abbr in self.g.objects(s, self.QUDT.abbreviation):
                qu.set_abbr(str(abbr))
            for quantity_kind in self.g.objects(s, self.QUDT.quantityKind):
                qu.set_quantity_kind(quantity_kind)
            for conversion_multiplier in self.g.objects(s, self.QUDT.conversionMultiplier):
                qu.set_conversion_multiplier(float(conversion_multiplier))
            for conversion_offset in self.g.objects(s, self.QUDT.conversionOffset):
                qu.set_conversion_offset(float(conversion_offset))

            yield qu
