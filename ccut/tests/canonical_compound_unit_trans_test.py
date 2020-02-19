from ..main.ccut_main import CanonicalCompoundUnitTransformation_Main as ccut_main

def test():

    s = ccut_main.get_instance()

    # Basic Compund Unit Flow
    a_oval, a_err, _, _, _ = s.convert_str2str("km s^2", "hr^2 microft", 0.123)
    e_oval, e_err = 31.13760, 0
    assert a_err == e_err
    assert abs(a_oval - e_oval) < 0.001


    # Basic Single Unit Flow
    a_oval, a_err, _, _, _ = s.convert_str2str("degC", "degF", 13.33)
    e_oval, e_err = (55.99733, 0)
    assert (a_err == e_err)
    assert abs(a_oval - e_oval) < 0.001


    # DIFFDIM #1 Single Unit Flow
    a_oval, a_err, _, _, _ = s.convert_str2str("ha^2", "km^4", 3.049)
    e_oval, e_err = 0.0003049, 0
    assert a_err == e_err
    assert abs(a_oval - e_oval) < 0.00001

    # DIFFDIM #2 Single Unit Flow
    a_oval, a_err, _, _, _ = s.convert_str2str("km^3", "mliter", 3.049)
    e_oval, e_err = 3049000000000000, 0
    assert a_err == e_err
    assert abs(a_oval - e_oval) < 0.01


    # TRANSFORMATION_IS_NOT_SYMMETRIC Error flow
    a_oval, a_err, _, _, _ = s.convert_str2str("degC km", "K ft", 0.234)
    e_err = 1
    assert (a_err == e_err)

    # DIMENSION_MISMATCH Error flow
    a_oval, a_err, _, _, _ = s.convert_str2str("km", "s", 124)
    e_err = 2
    assert (a_err == e_err)

    # TRANSFORMATION_UNKNOWN Error flow
    a_oval, a_err, _, _, _ = s.convert_str2str("km s", "ft hr X", 267)
    e_err = 3
    assert (a_err == e_err)
    a_oval, a_err, _, _, _ = s.convert_str2str("km s X", "ft hr", 7226)
    assert (a_err == e_err)