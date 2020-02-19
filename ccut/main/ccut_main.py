'''
The Main callable
'''

from .canonical_compound_unit import CanonicalCompoundUnit
from .canonical_compound_unit_transformation import CanonicalCompoundUnitTransformation, RET_STR_MAP, RET_VAL_OK, \
    RET_VAL_TRANS_NOT_SYMMETRIC, RET_VAL_DIMENSION_MISMATCH, RET_VAL_TRANS_UNKNOWN, RET_VAL_UNSUPPORTED_FLOW
from .unit_visitor import UnitVisitor
from arpeggio import visit_parse_tree

# Use as singleton class
class CanonicalCompoundUnitTransformation_Main:
    instance = None

    def __init__(self):
        self.ccut_inst = CanonicalCompoundUnitTransformation()
        
    @staticmethod
    def get_instance() -> 'CanonicalCompoundUnitTransformation_Main':
        if CanonicalCompoundUnitTransformation_Main.instance is None:
            CanonicalCompoundUnitTransformation_Main.instance = CanonicalCompoundUnitTransformation_Main()

        return CanonicalCompoundUnitTransformation_Main.instance

    def get_top_ccu(self, unit_string):
        ccu = self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_string)
        return ccu

    def get_all_ccu(self, unit_string):
        # TBD
        return None

    def convert_ccu2ccu(self, ccu_src, ccu_dst, val_in):
        num_out, sts = self.ccut_inst.canonical_transform(ccu_src, ccu_dst, val_in)
        return num_out, sts, RET_STR_MAP[sts]

    def convert_str2str(self, unit_src_string, unit_dst_string, val_in):
        # get canonical representation
        ccu_src = self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_src_string)
        ccu_dst = self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_dst_string)
        
        num_out, sts, sts_str = self.convert_ccu2ccu(ccu_src, ccu_dst, val_in)
        return num_out, sts, sts_str, ccu_src, ccu_dst