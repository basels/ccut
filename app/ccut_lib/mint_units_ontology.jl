{
  "@context": {
    "ccut": "https://basels.github.io/ccut_onto/ccut.ttl#",
    "qudt": "http://www.qudt.org/qudt/owl/1.0.0/qudt/#",
    "qudtp": "http://www.qudt.org/qudt/owl/1.0.0/qudt/Properties.html#",
    "qudtu": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "ccut:prefixConversionMultiplier",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates an SI (International System of Units) Prefix Multiplier to some atomic unit"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Prefix Conversion Multiplier"
      },
      "rdfs:range": {
        "@id": "xsd:double"
      }
    },
    {
      "@id": "ccut:hasPart",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates a compound unit with atomic units that compose it"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Has Part"
      },
      "rdfs:range": {
        "@id": "ccut:atomicUnit"
      }
    },
    {
      "@id": "ccut:prefix",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates an SI (International System of Units) Prefix URI to some atomic unit"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Prefix"
      },
      "rdfs:range": {
        "@id": "qudt:QuantityKind"
      }
    },
    {
      "@id": "ccut:prefixConversionOffset",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates an SI (International System of Units) Prefix Offset to some atomic unit"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Prefix Conversion Offset"
      },
      "rdfs:range": {
        "@id": "xsd:double"
      }
    },
    {
      "@id": "ccut:hasDimension",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates an atomic or compound unit with a dimension string"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Has Dimension"
      },
      "rdfs:range": {
        "@id": "xsd:string"
      }
    },
    {
      "@id": "ccut:multiplier",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates a multiplier (dimension prefix multiplier) to some atomic unit"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Multiplier"
      },
      "rdfs:range": {
        "@id": "xsd:double"
      }
    },
    {
      "@id": "ccut:compoundUnit",
      "@type": "rdfs:Class",
      "ccut:hasDimension": {
        "@id": "xsd:string"
      },
      "ccut:hasPart": {
        "@id": "ccut:atomicUnit"
      },
      "qudtp:abbreviation": {
        "@id": "xsd:string"
      },
      "rdfs:comment": {
        "@language": "en",
        "@value": "A class to represent a complex unit that is composed from two or more atomic units with some relationship between them"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Compound Unit"
      }
    },
    {
      "@id": "ccut:exponent",
      "@type": "rdf:Property",
      "rdfs:comment": {
        "@language": "en",
        "@value": "Associates an exponent (dimension exponent) to some atomic unit"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Exponent"
      },
      "rdfs:range": {
        "@id": "xsd:double"
      }
    },
    {
      "@id": "ccut:atomicUnit",
      "@type": "rdfs:Class",
      "ccut:exponent": {
        "@id": "xsd:double"
      },
      "ccut:hasDimension": {
        "@id": "xsd:string"
      },
      "ccut:multiplier": {
        "@id": "xsd:double"
      },
      "ccut:prefix": {
        "@id": "qudt:QuantityKind"
      },
      "ccut:prefixConversionMultiplier": {
        "@id": "xsd:double"
      },
      "ccut:prefixConversionOffset": {
        "@id": "xsd:double"
      },
      "qudtp:conversionMultiplier": {
        "@id": "xsd:double"
      },
      "qudtp:conversionOffset": {
        "@id": "xsd:double"
      },
      "qudtp:quantityKind": {
        "@id": "qudt:QuantityKind"
      },
      "qudtp:symbol": {
        "@id": "xsd:string"
      },
      "rdfs:comment": {
        "@language": "en",
        "@value": "A class to represent a single unit symbol which may be modified by additional elements such as exponents or prefixes"
      },
      "rdfs:label": {
        "@language": "en",
        "@value": "Atomic Unit"
      }
    }
  ]
}