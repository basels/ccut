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
from ccut import ccut
cc = ccut()
```

#### CCU Representation:
##### `get_top_ccu`:
This method is used to get the top (single) CCU representation (dictionary) for a given string.<br />
Run with a single argument (string of atomic/compound unit).<br />
For example, running:
```
cc.get_top_ccu("kg/s^2")
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

##### `get_all_ccu`:
This method is used to get all the (multiple) CCU representations (ordered list of dictionaries) for a given string.<br />
Run with a single argument (string of atomic/compound unit).<br />
For example, running:
```
cc.get_all_ccu("oz")
```
Will return:
```
TBD
```

#### CCU Transformation (Conversion):
##### `convert_ccu2ccu`:
This method is used to perfrom compound unit conversion given the CCU representations.<br />
Run with three arguments (ccu representation of the source unit, ccu representation of the destination unit, value to transform).<br />
This method will return 3 values:
- the value after conversion
- the return status (see below)
- the return status in readable format (string)
Where:
```
# Status key: 0: "OK"
#             1: "TRANSFORMATION_IS_NOT_SYMMETRIC"
#             2: "DIMENSION_MISMATCH"
#             3: "TRANSFORMATION_UNKNOWN"
#             4: "UNSUPPORTED_FLOW"
```
For example, running:
```
src_ccu = cc.get_top_ccu("m/s")
dst_ccu = cc.get_top_ccu("mi/hr")
cc.convert_str2str(src_ccu, dst_ccu, 2.7)
```
Will return:
```
(6.039727988546887, 0, 'OK')
```

##### `convert_str2str`:
This method is used to perfrom compound unit conversion given the strings of the source and destination units.<br />
Run with three arguments (string of source unit, string of destination unit, value to transform).<br />
This method will return 5 values:
- the value after conversion
- the return status
- the return status in readable format (string)
- CCU representaiton of the source string
- CCU representaiton of the destination string
For example, running:
```
cc.convert_str2str("m/s", "mi/hr", 2.7)
```
Will return:
```
(
    6.039727988546887,
    0,
    'OK',
    {
        'qudtp:abbreviation': 'm s-1',
        'ccut:hasPart': [
            {
                'qudtp:symbol': 'm',
                'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Meter',
                'ccut:hasDimension': 'L',
                'qudtp:conversionMultiplier': 1.0,
                'qudtp:conversionOffset': 0.0,
                '_metadata:total_dimension': 1.0
            },
            {
                'qudtp:symbol': 's',
                'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#SecondTime',
                'ccut:hasDimension': 'T',
                'qudtp:conversionMultiplier': 1.0,
                'qudtp:conversionOffset': 0.0,
                'ccut:exponent': '-1',
                '_metadata:total_dimension': -1.0
            }
        ],
        'ccut:hasDimension': 'L T-1'
    },
    {
        'qudtp:abbreviation': 'mi hr-1',
        'ccut:hasPart': [
            {
                'qudtp:symbol': 'mi',
                'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#MileInternational',
                'ccut:hasDimension': 'L',
                'qudtp:conversionMultiplier': 1609.344,
                'qudtp:conversionOffset': 0.0
            },
            {
                'qudtp:symbol': 'hr',
                'qudtp:quantityKind': 'http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Hour',
                'ccut:hasDimension': 'T',
                'qudtp:conversionMultiplier': 3600.0,
                'qudtp:conversionOffset': 0.0,
                'ccut:exponent': '-1'
            }
        ],
        'ccut:hasDimension': 'L T-1'
    }
)
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