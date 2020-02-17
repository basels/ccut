## Canonicalization Compound Unit Representation & Transformation (CCUT)
- Identifying individual units, their exponents and multipliers
- Representing units in a canonical format
- Mapping units to Ontology
- Finding the dimensions of each atomic unit
- Converting from one unit to another

This is the implementation accompanying the MWS 2019 paper, [_Parsing, Representing and Transforming Units of Measure_](https://www.momacs.pitt.edu/wp-content/uploads/2019/05/Parsing-Representing-and-Transforming-Units-of-Measure.pdf).

### How to run:
Here's how you can use this library. Import the module and then create an instance:

```
from ccut import CCUT

myccut_inst = CCUT()
```

#### > CCU Representation:
Run `ccu_repr` with a single argument (string of atomic/compound unit).

For example, running:
```
myccut_inst.ccu_repr("kg/s^2")
```
Will return:
```
{
    'qudtp:abbreviation': 'kg s-2',
    'ccut:hasPart': [
        {
            'qudtp:symbol': 'kg',
            'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Gram',
            'ccut:prefix': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Kilo', 'ccut:prefixConversionMultiplier': 1000.0,
            'ccut:prefixConversionOffset': 0.0,
            'ccut:hasDimension': 'M',
            'qudtp:conversionMultiplier': 0.001,
            'qudtp:conversionOffset': 0.0
        },
        {
            'qudtp:symbol': 's',
            'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#SecondTime',
            'ccut:hasDimension': 'T',
            'qudtp:conversionMultiplier': 1.0,
            'qudtp:conversionOffset': 0.0,
            'ccut:exponent': '-2'
        }
    ],
    'ccut:hasDimension': 'M T-2'
}
```

#### > CCU Transformation (Conversion):
Run `canonical_transform` with three arguments (string of source unit, string of destination unit, value to transform).

For example, running:
```
myccut_inst.canonical_transform("m/s", "mi/hr", 2.7)
```
Will return:
```
(6.039727988546887, 0)
```
The first value in the tuple is the value after conversion, the second is the return code, where:
```
# Error key: 0: "OK"
#            1: "TRANSFORMATION_IS_NOT_SYMMETRIC"
#            2: "DIMENSION_MISMATCH"
#            3: "TRANSFORMATION_UNKNOWN"
#            4: "UNSUPPORTED_FLOW"
```

### Citing CCUT
If you would like to cite the this tool in a paper or presentation, the following is recommended (BibTeX entry):
```
@article{shbita2019parsing,
  title={Parsing, Representing and Transforming Units of Measure},
  author={Shbita, Basel and Rajendran, Arunkumar and Pujara, Jay and Knoblock, Craig A}
  journal={Modeling the World’s Systems},
  year={2019},
}
```