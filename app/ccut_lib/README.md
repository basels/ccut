# Canonicalization Compound Unit Representation & Transformation
- Identifying individual units, their exponents and multipliers
- Representing units in a canonical format
- Mapping units to Ontology
- Finding the dimensions of each atomic unit
- Converting from one unit to another

### How to run:
Here are the different ways you can use this library:
#### > Web Form:
```
export FLASK_APP=main.api && flask run
```
Navigate to ```http://localhost:localport/trans_form``` and use form
#### > Web API:
HTTP GET Request:
```http://localhost:localport/trans_form?in_unit=km&out_unit=ft&in_val=0.3049```
#### Output:
format is ```jsonify(canonical_json_in, canonical_json_out, out_val, error_enum, error_string)```
example:
```
[ {
    ccut:hasPart: [ ... ],
    ccut:hasDimension: "L",
    qudtp:abbreviation: "km"
  },
  {
    ccut:hasPart: [ ... ],
    qudtp:abbreviation: "ft",
    ...
  },
  6561.679790026246,
  0,
  "OK" ]
```
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