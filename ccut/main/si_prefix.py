'''
The SIPrefix class defines the SI (International System of Units) prefixes
and the different variants that are used to symbolize the same prefix.
'''

class SIPrefix:
    name_factor = {
        "deci": 1e-1,
        "centi": 1e-2,
        "milli": 1e-3,
        "micro": 1e-6,
        "nano": 1e-9,
        "pico": 1e-12,
        "femto": 1e-15,
        "atto": 1e-18,
        "zepto": 1e-21,
        "yocto": 1e-24,
        "deca": 1e1,
        "hecto": 1e2,
        "kilo": 1e3,
        "mega": 1e6,
        "giga": 1e9,
        "tera": 1e12,
        "peta": 1e15,
        "exa": 1e18,
        "zetta": 1e21,
        "yotta": 1e24,
    }

    symbol_factor = {
        "d": 1e-1,
        "c": 1e-2,
        "m": 1e-3,
        "µ": 1e-6,
        "mu": 1e-6,
        "micro": 1e-6,  # Exception for micro since the symbol is a greek letter
        "n": 1e-9,
        "p": 1e-12,
        "f": 1e-15,
        "a": 1e-18,
        "z": 1e-21,
        "y": 1e-24,
        "da": 1e1,
        "h": 1e2,
        "k": 1e3,
        "M": 1e6,
        "G": 1e9,
        "T": 1e12,
        "P": 1e15,
        "E": 1e18,
        "Z": 1e21,
        "Y": 1e24
    }

    @classmethod
    def get_factor(cls, prefix):
        if prefix.lower() in cls.name_factor:
            return cls.name_factor[prefix.lower()]
        elif prefix in cls.symbol_factor:
            return cls.symbol_factor[prefix]

        return None

    @classmethod
    def is_si_prefix(cls, prefix):
        return (prefix.lower() in cls.name_factor or prefix in cls.symbol_factor)
