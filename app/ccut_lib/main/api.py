from arpeggio import visit_parse_tree
from flask import Flask, request, jsonify, render_template, url_for, flash
from main.unit_parser import UnitParser
from main.unit_visitor import UnitVisitor
from main.canonical_compound_unit import CanonicalCompoundUnit
############ Web Forms ############
from main.forms import TransformationForm
from main.config import Config
############ mappings and unit-match UT ############
from main.unit_match import UnitMatch
from main.symbol_map import SymbolMap
from main.dimension_map import DimensionMap
from main.canonical_compound_unit_transformation import CanonicalCompoundUnitTransformation
############

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def hello():
    return render_template('generic.html', data='Welcome to MINT CCUT!')

@app.route("/get_symbol_map")
def get_symbol_map():
    s = SymbolMap.get_instance()
    return jsonify(list(s.symbol_map), list(s.label_map), list(s.si_prefix_map))

@app.route("/get_dimension_map")
def get_dimension_map():
    d = DimensionMap.get_instance()
    return jsonify(d.qd_map)

@app.route("/best_unit_match")
def best_unit_match_test():
    s = SymbolMap.get_instance()
    unit_string = request.args.get("u")
    unit = UnitMatch.find_best_unit_match(unit_string, s)
    return jsonify(unit)

@app.route("/get_canonical_json")
def get_canonical_json():
    unit_string = request.args.get("u")

    parser = UnitParser().get_parser()
    parsed_unit = visit_parse_tree(parser.parse(unit_string), UnitVisitor(debug=False))
    canonical_json = CanonicalCompoundUnit(parsed_unit).get_unit_object()

    return jsonify(canonical_json)

@app.route('/trans_form', methods=['GET', 'POST'])
def transform_ccu():
    if "in_unit" in request.args and "out_unit" in request.args and "in_val" in request.args:
        unit_in_string = request.args.get("in_unit")
        unit_out_string = request.args.get("out_unit")
        val_in = float(request.args.get("in_val"))
        return canonical_transform(unit_in_string, unit_out_string, val_in)
    
    # if form.validate_on_submit():
    #    flash('Transformation requested for in_unit {}, out_unit={}, in_val={}'.format(
    #        form.in_unit.data, form.out_unit.data, form.in_val.data))
    #    return canonical_transform(form.in_unit.data, form.out_unit.data, form.in_val.data)

    # we can parse the return object using:
    # return render_template('generic.html', data=some_obj.get_data().decode("utf-8"))

    form = TransformationForm()
    return render_template('ccu_transform.html', title='Canonical Transform', form=form)

def canonical_transform(unit_in_string, unit_out_string, val_in):

    s = CanonicalCompoundUnitTransformation.get_instance()

    canonical_json_in, canonical_json_out = s.get_canonical_json_reprs(unit_in_string, unit_out_string)
    num_out, error = s.canonical_transform(unit_in_string, unit_out_string, val_in)

    # for easier debug print error meaning
    ret_str_map = ["OK", "TRANSFORMATION_IS_NOT_SYMMETRIC", "DIMENSION_MISMATCH", "TRANSFORMATION_UNKNOWN", "UNSUPPORTED_FLOW"]
    error_string = ret_str_map[error]
    return jsonify(canonical_json_in, canonical_json_out, num_out, error, error_string)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
