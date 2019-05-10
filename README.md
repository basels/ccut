## Canonicalization Compound Unit Representation & Transformation via Docker HTTP endpoint

### How to run:
#### Build image
```
docker build -t ccut_img .
```
#### Run image (flask server)
```
docker run -d -p 5000:5000 ccut_img run -h 0.0.0.0 -p 5000
```

### Examples:
#### Get Unit Representation
```
curl -X GET "http://0.0.0.0:5000/get_canonical_json?u=km%20s^2"
```
Output format is ```JSON: canonical_json```
```
{
    ccut:hasDimension: "L T2",
    ccut:hasPart: [
        {
            ccut:hasDimension: "L",
            ccut:prefix: "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Kilo",
            ccut:prefixConversionMultiplier: 1000.0,
            ccut:prefixConversionOffset: 0.0,
            qudtp:conversionMultiplier: 1.0,
            qudtp:conversionOffset: 0.0,
            qudtp:quantityKind: "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#Meter",
            qudtp:symbol: "km"
        },
        {
            ccut:exponent: "2",
            ccut:hasDimension: "T",
            qudtp:conversionMultiplier: 1.0,
            qudtp:conversionOffset: 0.0,
            qudtp:quantityKind: "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#SecondTime",
            qudtp:symbol: "s"
        }
    ],
    qudtp:abbreviation: "km s2"
}
```
#### Get Units Transformation
```
curl -X GET "http://0.0.0.0:5000/trans_form?in_unit=km&out_unit=ft&in_val=0.3049"
```
Output format is ```JSON :canonical_json_in, canonical_json_out, out_val, error_enum, error_string```
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