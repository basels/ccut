## Canonicalization Compound Unit Representation & Transformation
- Identifying individual units, their exponents and multipliers
- Representing units in a canonical format
- Mapping units to Ontology
- Finding the dimensions of each atomic unit
- Converting from one unit to another

This is the implementation accompanying the MWS 2019 paper, [_Parsing, Representing and Transforming Units of Measure_](https://www.momacs.pitt.edu/wp-content/uploads/2019/05/Parsing-Representing-and-Transforming-Units-of-Measure.pdf).

### How to run:
Here's how you can use this library:

#### > Python API:
```
from ... import CanonicalCompoundUnitTransformation
s = CanonicalCompoundUnitTransformation.get_instance()
val_out, error = s.canonical_transform(unit_in_string, unit_out_string, val_in)

# Error key: 0: "OK"
#            1: "TRANSFORMATION_IS_NOT_SYMMETRIC"
#            2: "DIMENSION_MISMATCH"
#            3: "TRANSFORMATION_UNKNOWN"
#            4: "UNSUPPORTED_FLOW"

# Example: canonical_transform(x, "km s^2", "hr^2 microft"): return x*253.151, 0
```

### Running Tests:
We use the pytest package as the base framework for our tests:
```
pytest -v
```