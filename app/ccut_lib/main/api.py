''' This is the API entry point (and Flask front end) '''

from arpeggio import visit_parse_tree
from flask import Flask, request, jsonify, render_template
from main.forms import TransformationForm, RepresentationForm
from main.canonical_compound_unit import CanonicalCompoundUnit
from main.canonical_compound_unit_transformation import CanonicalCompoundUnitTransformation, RET_STR_MAP
from main.config import Config
from main.dimension_map import DimensionMap
from main.symbol_map import SymbolMap
from main.unit_match import UnitMatch
from main.unit_parser import UnitParser
from main.unit_visitor import UnitVisitor

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

@app.route('/get_canonical_json', methods=['GET', 'POST'])
def get_canonical_json():
    if "u" in request.args:
        unit_string = request.args.get("u")
        return ccu_repr(unit_string)
    form = RepresentationForm()
    return render_template('ccu_represent.html', title='Canonical Representation', form=form)
        
def ccu_repr(unit_string):
    parser = UnitParser().get_parser()
    parsed_unit = visit_parse_tree(parser.parse(unit_string), UnitVisitor(debug=False))
    ccu = CanonicalCompoundUnit(parsed_unit).get_unit_object()
    return jsonify(ccu)

@app.route('/trans_form', methods=['GET', 'POST'])
def transform_ccu():
    if "in_unit" in request.args and "out_unit" in request.args and "in_val" in request.args:
        unit_in_string = request.args.get("in_unit")
        unit_out_string = request.args.get("out_unit")
        val_in = float(request.args.get("in_val"))
        return ccu2ccu_transform(unit_in_string, unit_out_string, val_in)
    form = TransformationForm()
    return render_template('ccu_transform.html', title='Canonical Transform', form=form)

def ccu2ccu_transform(unit_src_string, unit_dst_string, val_in):
    s = CanonicalCompoundUnitTransformation.get_instance()
    ccu_src = s.get_canonical_compound_unit_dict_from_string(unit_src_string)
    ccu_dst = s.get_canonical_compound_unit_dict_from_string(unit_dst_string)
    num_out, error = s.canonical_transform(unit_src_string, unit_dst_string, val_in)
    return jsonify(ccu_src, ccu_dst, num_out, error, RET_STR_MAP[error])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
