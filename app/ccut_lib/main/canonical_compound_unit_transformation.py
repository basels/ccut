'''
The CanonicalCompoundUnitTransformation class is used to perform
unit conversions between atomic and compound units of measurement (given as strings).
'''

from re import search
from arpeggio import visit_parse_tree
from main.unit_parser import UnitParser
from main.unit_visitor import UnitVisitor
from main.canonical_compound_unit import CanonicalCompoundUnit
from main.canonical_simple_unit import QUDT_PROPERTIES_NAMESPACE, CCUT_NAMESPACE

RET_VAL_OK = 0
RET_VAL_TRANS_NOT_SYMMETRIC = 1
RET_VAL_DIMENSION_MISMATCH = 2
RET_VAL_TRANS_UNKNOWN = 3
RET_VAL_UNSUPPORTED_FLOW = 4

# Use as singleton class
class CanonicalCompoundUnitTransformation:
    instance = None

    def __init__(self):
        self.parser = UnitParser().get_parser()

    @staticmethod
    def get_instance() -> 'CanonicalCompoundUnitTransformation':
        if CanonicalCompoundUnitTransformation.instance is None:
            CanonicalCompoundUnitTransformation.instance = CanonicalCompoundUnitTransformation()

        return CanonicalCompoundUnitTransformation.instance

    def canonical_transform_check_type_and_dim(self, part_type, part_dim):
        if ("UNKNOWN TYPE" == part_type) or ("UNKNOWN DIMENSION" == part_dim):
            return False, RET_VAL_TRANS_UNKNOWN
        return True, RET_VAL_OK

    def get_dimstr_dimexp_from_dimension(self, dim_string):
        tot_exp = 1
        tot_str = dim_string

        curr_dim_in_exp_re = search("\d", dim_string)
        if curr_dim_in_exp_re:
            tot_dim_idx = curr_dim_in_exp_re.start()
            tot_str = dim_string[:tot_dim_idx]
            try:
                tot_exp = int(dim_string[tot_dim_idx:])
            except:
                tot_str = dim_string
                tot_exp = 1

        return tot_str, tot_exp

    def get_canonical_json_reprs(self, unit_in_string, unit_out_string):
        # parse input and output units
        parsed_input_unit = visit_parse_tree(self.parser.parse(unit_in_string), UnitVisitor(debug=False))
        parsed_output_unit = visit_parse_tree(self.parser.parse(unit_out_string), UnitVisitor(debug=False))
        
        # get canonical representation
        canonical_json_in = CanonicalCompoundUnit(parsed_input_unit).get_unit_object()
        canonical_json_out = CanonicalCompoundUnit(parsed_output_unit).get_unit_object()

        return canonical_json_in, canonical_json_out

    def canonical_transform(self, unit_in_string, unit_out_string, val_in):
        # get canonical representation
        canonical_json_in, canonical_json_out = self.get_canonical_json_reprs(unit_in_string, unit_out_string)

        # check if overall-dimensions match
        if canonical_json_in[f'{CCUT_NAMESPACE}:hasDimension'] != canonical_json_out[f'{CCUT_NAMESPACE}:hasDimension']:
            return 0.0, RET_VAL_DIMENSION_MISMATCH # ERROR

        # create a copy of the output-required-parts
        cncl_out_pts_cpy = list(canonical_json_out[f'{CCUT_NAMESPACE}:hasPart'])

        num_in = float(val_in)

        uout = num_in
        accu_str = ('C = IN = %f\n' % uout)

        in_len = len(canonical_json_in[f'{CCUT_NAMESPACE}:hasPart'])
        accu_offset = 0
        feedback_str = RET_VAL_OK

        # iterate over each part in the INPUT-canonical-unit
        for idx_in, pt_in in enumerate(canonical_json_in[f'{CCUT_NAMESPACE}:hasPart'], start=0):

            # check current Input type and dimension
            curr_type_in  = pt_in[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind']
            curr_dim_in   = pt_in[f'{CCUT_NAMESPACE}:hasDimension']

            uin_power = 1.0
            if 'ccut:exponent' in pt_in:
                uin_power = int(pt_in['ccut:exponent'])

            dimstr_in, dimexp_in = self.get_dimstr_dimexp_from_dimension(curr_dim_in)
            pt_in['_metadata:total_dimension'] = dimexp_in * uin_power

            check_pt, tmp_str = self.canonical_transform_check_type_and_dim(curr_type_in, curr_dim_in)
            if False == check_pt:
                return 0.0, tmp_str # ERROR
            curr_pt_out = None

            # iterate over each part in the OUTPUT-canonical-unit-copy
            for idx_out, pt_out in enumerate(cncl_out_pts_cpy, start=0):

                u_out_power = 1.0
                if f'{CCUT_NAMESPACE}:exponent' in pt_out:
                    u_out_power = int(pt_out[f'{CCUT_NAMESPACE}:exponent'])

                curr_dim_out  = pt_out[f'{CCUT_NAMESPACE}:hasDimension']

                dimstr_out, dimexp_out = self.get_dimstr_dimexp_from_dimension(curr_dim_out)
                pt_out['_metadata:total_dimension'] = dimexp_out * u_out_power

                if pt_in['_metadata:total_dimension'] == pt_out['_metadata:total_dimension']:
                    curr_pt_out = pt_out.copy()
                    del cncl_out_pts_cpy[idx_out]
                    break

            # ERROR: we didn't find an output unit
            #        THIS MEANS THERE IS A PROBLEM IN THE CODE, SINCE WE 'PASSED' OVERALL-DIMENSIONS CHECK
            if None == curr_pt_out:
                return 0.0, RET_VAL_UNSUPPORTED_FLOW # ERROR

            # calcuate to match input prefix
            uin_no_prfx = uout
            accu_str += 'A = C = %f\n' % uin_no_prfx

            if f'{CCUT_NAMESPACE}:prefix' in pt_in:
                prfx_conv_mult = pt_in[f'{CCUT_NAMESPACE}:prefixConversionMultiplier']
                prfx_conv_offs = pt_in[f'{CCUT_NAMESPACE}:prefixConversionOffset']
                uin_no_prfx = (uin_no_prfx * pow(prfx_conv_mult, uin_power)) + prfx_conv_offs
                accu_offset += prfx_conv_offs
                accu_str += 'A = (A * %f^%f) + %f\n' % (prfx_conv_mult, uin_power, prfx_conv_offs)
            qu_in_conv_mult  = pt_in[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier']
            qu_in_conv_off   = pt_in[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset']
            qu_out_conv_mult = curr_pt_out[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier']
            qu_out_conv_off  = curr_pt_out[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset']
            # calculate input --> base, base --> output
            uin_to_base  = (uin_no_prfx * pow(qu_in_conv_mult, uin_power)) + qu_in_conv_off
            accu_offset += qu_in_conv_off
            accu_str += 'B = (A * %f^%f) + %f\n' % (qu_in_conv_mult, uin_power, qu_in_conv_off)
            uout = (uin_to_base - qu_out_conv_off) / pow(qu_out_conv_mult, u_out_power)
            accu_offset += qu_out_conv_off
            accu_str += 'C = (B - %f) / %f^%f\n' % (qu_out_conv_off, qu_out_conv_mult, u_out_power)
            # calcuate to match output prefix
            if f'{CCUT_NAMESPACE}:prefix' in curr_pt_out:
                prfx_conv_mult = curr_pt_out[f'{CCUT_NAMESPACE}:prefixConversionMultiplier']
                prfx_conv_offs = curr_pt_out[f'{CCUT_NAMESPACE}:prefixConversionOffset']
                uout = (uout - prfx_conv_offs) / pow(prfx_conv_mult, u_out_power)
                accu_offset += prfx_conv_offs
                accu_str += 'C = (C - %f) / %f^%f\n' % (prfx_conv_offs, prfx_conv_mult, u_out_power)
            accu_str += 'C = %f\n' % uout

        # print(accu_str)

        # check if there are still 'parts' in the output, if so, then we can't perform the transformation
        if len(cncl_out_pts_cpy) > 0:
            return 0.0, RET_VAL_TRANS_UNKNOWN # ERROR

        # check if we had a transformation that required an offset addition or subtraction in a multi-transformation process
        if 0 != accu_offset and in_len > 1:
            return 0.0, RET_VAL_TRANS_NOT_SYMMETRIC # ERROR

        return uout, feedback_str
