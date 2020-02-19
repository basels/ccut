'''
The CanonicalCompoundUnitTransformation class is used to perform
unit conversions between atomic and compound units of measurement (given as strings).
'''

from arpeggio import visit_parse_tree
from copy import deepcopy
from .canonical_compound_unit import CanonicalCompoundUnit
from .canonical_simple_unit import QUDT_PROPERTIES_NAMESPACE, CCUT_NAMESPACE
from .unit_parser import UnitParser
from .unit_visitor import UnitVisitor
from re import search

RET_STR_MAP = ["OK", "TRANSFORMATION_IS_NOT_SYMMETRIC", "DIMENSION_MISMATCH", "TRANSFORMATION_UNKNOWN", "UNSUPPORTED_FLOW"]
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
            # TODO: revisit this
            try:
                tot_exp = int(dim_string[tot_dim_idx:])
            except:
                tot_str = dim_string
                tot_exp = 1

        return tot_str, tot_exp

    def get_canonical_compound_unit_dict_from_string(self, unit_string):
        # parse input and output units
        parsed_unit = visit_parse_tree(self.parser.parse(unit_string), UnitVisitor(debug=False))
        canonical_compound_unit_dict = CanonicalCompoundUnit(parsed_unit).get_unit_object()
        return canonical_compound_unit_dict

    def get_atomic_unit_exponent(self, atomic_unit_part_dict):
        exponent = 1.0
        exponent_index_str = f'{CCUT_NAMESPACE}:exponent'
        if exponent_index_str in atomic_unit_part_dict:
            exponent = float(atomic_unit_part_dict[exponent_index_str])
        return exponent

    def get_atomic_unit_multiplier(self, atomic_unit_part_dict):
        multiplier = 1.0
        multiplier_index_str = f'{CCUT_NAMESPACE}:multiplier'
        if multiplier_index_str in atomic_unit_part_dict:
            multiplier = float(atomic_unit_part_dict[multiplier_index_str])
        return multiplier

    def get_atomic_unit_symbol(self, atomic_unit_part_dict):
        symbol_index_str = f'{QUDT_PROPERTIES_NAMESPACE}:symbol'
        return atomic_unit_part_dict[symbol_index_str]

    def get_compound_unit_parts(self, compound_unit_dict):
        parts_index_str = f'{CCUT_NAMESPACE}:hasPart'
        if parts_index_str in compound_unit_dict:
            return compound_unit_dict[parts_index_str]
        return None

    def normalize_src_dst_compound_units(self, compound_unit_dict_src, compound_unit_dict_dst):
        compound_unit_dict_src_copy = deepcopy(compound_unit_dict_src)

        atomic_idx_src_orig = 0 # used since we alter src_copy but we must maintain the src index
        for atomic_idx_src, atomic_pt_src in enumerate(self.get_compound_unit_parts(compound_unit_dict_src_copy)):

            src_pt_type  = atomic_pt_src[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind']
            src_pt_dim   = atomic_pt_src[f'{CCUT_NAMESPACE}:hasDimension']
            src_pt_exp   = self.get_atomic_unit_exponent(atomic_pt_src)
            src_pt_smbl  = self.get_atomic_unit_symbol(atomic_pt_src)
            src_pt_mlt   = self.get_atomic_unit_multiplier(atomic_pt_src)

            ''' iterate over dst compound unit and check
            if we have a an atomic unit with the same symbol and exponent '''
            compound_unit_dict_dst_copy = deepcopy(compound_unit_dict_dst)
            for atomic_idx_dst, atomic_pt_dst in enumerate(self.get_compound_unit_parts(compound_unit_dict_dst_copy)):
                dst_pt_type  = atomic_pt_src[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind']
                dst_pt_dim   = atomic_pt_src[f'{CCUT_NAMESPACE}:hasDimension']
                dst_pt_exp   = self.get_atomic_unit_exponent(atomic_pt_dst)
                dst_pt_smbl  = self.get_atomic_unit_symbol(atomic_pt_dst)
                dst_pt_mlt   = self.get_atomic_unit_multiplier(atomic_pt_dst)

                dst_type_dim_valid, _ = self.canonical_transform_check_type_and_dim(dst_pt_type, dst_pt_dim)
                if src_pt_smbl == dst_pt_smbl and src_pt_exp == dst_pt_exp and src_pt_mlt == dst_pt_mlt:
                    self.get_compound_unit_parts(compound_unit_dict_src).pop(atomic_idx_src_orig)
                    atomic_idx_src_orig -= 1
                    self.get_compound_unit_parts(compound_unit_dict_dst).pop(atomic_idx_dst)
                    break
            atomic_idx_src_orig += 1

    def canonical_transform(self, ccu_src, ccu_dst, val_in):

        # check if overall-dimensions match
        if ccu_src[f'{CCUT_NAMESPACE}:hasDimension'] != ccu_dst[f'{CCUT_NAMESPACE}:hasDimension']:
            return 0.0, RET_VAL_DIMENSION_MISMATCH # ERROR

        ''' if we reached here it means that dimensions match even if some are not recognized!
            i.e.: 'USD' (part) has "UNKNOWN DIMENSION" and "UNKNOWN TYPE" / other part is 'kg' -->
                  abbreviation of the whole unit "USD kg-1" '''
        self.normalize_src_dst_compound_units(ccu_src, ccu_dst)

        # create a copy of the output-required-parts
        ccu_dst_copy = deepcopy(self.get_compound_unit_parts(ccu_dst))

        num_in = float(val_in)
        uout = num_in

        src_len = len(self.get_compound_unit_parts(ccu_src))
        accu_offset = 0
        feedback_str = RET_VAL_OK

        # iterate over each part in the INPUT-canonical-unit
        for atomic_pt_src in self.get_compound_unit_parts(ccu_src):

            # check current input type and dimension
            curr_type_in  = atomic_pt_src[f'{QUDT_PROPERTIES_NAMESPACE}:quantityKind']
            curr_dim_in   = atomic_pt_src[f'{CCUT_NAMESPACE}:hasDimension']
            uin_power     = self.get_atomic_unit_exponent(atomic_pt_src)
            curr_mlt_in   = self.get_atomic_unit_multiplier(atomic_pt_src)

            dimstr_in, dimexp_in = self.get_dimstr_dimexp_from_dimension(curr_dim_in)
            atomic_pt_src['_metadata:total_dimension'] = dimexp_in * uin_power

            check_pt, tmp_str = self.canonical_transform_check_type_and_dim(curr_type_in, curr_dim_in)
            if False == check_pt:
                return 0.0, tmp_str # ERROR
            curr_atomic_pt_dst = None

            # iterate over each part in the OUTPUT-canonical-unit-copy
            for atomic_idx_dst, atomic_pt_dst in enumerate(ccu_dst_copy):

                u_out_power = self.get_atomic_unit_exponent(atomic_pt_dst)
                curr_dim_out  = atomic_pt_dst[f'{CCUT_NAMESPACE}:hasDimension']
                curr_mlt_out  = self.get_atomic_unit_multiplier(atomic_pt_dst)

                dimstr_out, dimexp_out = self.get_dimstr_dimexp_from_dimension(curr_dim_out)
                atomic_pt_dst['_metadata:total_dimension'] = dimexp_out * u_out_power

                if atomic_pt_src['_metadata:total_dimension'] == atomic_pt_dst['_metadata:total_dimension']:
                    curr_atomic_pt_dst = deepcopy(atomic_pt_dst)
                    del ccu_dst_copy[atomic_idx_dst]
                    break

            # ERROR: we didn't find an output unit
            #        THIS MEANS THERE IS A PROBLEM IN THE CODE, SINCE WE 'PASSED' OVERALL-DIMENSIONS CHECK
            if None == curr_atomic_pt_dst:
                return 0.0, RET_VAL_UNSUPPORTED_FLOW # ERROR

            # calcuate to match input prefix
            uin_no_prfx = uout

            if f'{CCUT_NAMESPACE}:prefix' in atomic_pt_src:
                prfx_conv_mult = atomic_pt_src[f'{CCUT_NAMESPACE}:prefixConversionMultiplier']
                prfx_conv_offs = atomic_pt_src[f'{CCUT_NAMESPACE}:prefixConversionOffset']
                uin_no_prfx = (uin_no_prfx * pow(prfx_conv_mult, uin_power)) + prfx_conv_offs
                accu_offset += prfx_conv_offs
            uin_no_prfx = (uin_no_prfx * pow(curr_mlt_in, uin_power))
            qu_in_conv_mult  = atomic_pt_src[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier']
            qu_in_conv_off   = atomic_pt_src[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset']
            qu_out_conv_mult = curr_atomic_pt_dst[f'{QUDT_PROPERTIES_NAMESPACE}:conversionMultiplier']
            qu_out_conv_off  = curr_atomic_pt_dst[f'{QUDT_PROPERTIES_NAMESPACE}:conversionOffset']
            # calculate input --> base, base --> output
            uin_to_base  = (uin_no_prfx * pow(qu_in_conv_mult, uin_power)) + qu_in_conv_off
            accu_offset += qu_in_conv_off
            uout = (uin_to_base - qu_out_conv_off) / pow(qu_out_conv_mult, u_out_power)
            accu_offset += qu_out_conv_off
            uout = uout / pow(curr_mlt_out, u_out_power)
            # calcuate to match output prefix
            if f'{CCUT_NAMESPACE}:prefix' in curr_atomic_pt_dst:
                prfx_conv_mult = curr_atomic_pt_dst[f'{CCUT_NAMESPACE}:prefixConversionMultiplier']
                prfx_conv_offs = curr_atomic_pt_dst[f'{CCUT_NAMESPACE}:prefixConversionOffset']
                uout = (uout - prfx_conv_offs) / pow(prfx_conv_mult, u_out_power)
                accu_offset += prfx_conv_offs

        # check if there are still 'parts' in the output, if so, then we can't perform the transformation
        if len(ccu_dst_copy) > 0:
            return 0.0, RET_VAL_TRANS_UNKNOWN # ERROR

        # check if we had a transformation that required an offset addition or subtraction in a multi-transformation process
        if 0 != accu_offset and src_len > 1:
            return 0.0, RET_VAL_TRANS_NOT_SYMMETRIC # ERROR

        return uout, feedback_str
