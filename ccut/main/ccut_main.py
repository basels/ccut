'''
The Main callable
'''

from .canonical_compound_unit_transformation import CanonicalCompoundUnitTransformation, RET_STR_MAP, RET_VAL_OK, \
    RET_VAL_TRANS_NOT_SYMMETRIC, RET_VAL_DIMENSION_MISMATCH, RET_VAL_TRANS_UNKNOWN, RET_VAL_UNSUPPORTED_FLOW

# Use as singleton class
class CanonicalCompoundUnitTransformation_Main:
    instance = None

    def __init__(self):
        self.ccut_inst = CanonicalCompoundUnitTransformation()
        
    @staticmethod
    def get_instance() -> 'CanonicalCompoundUnitTransformation_Main':
        ''' Get the singleton instance of ccut. '''

        if CanonicalCompoundUnitTransformation_Main.instance is None:
            CanonicalCompoundUnitTransformation_Main.instance = CanonicalCompoundUnitTransformation_Main()
            
        return CanonicalCompoundUnitTransformation_Main.instance

    def get_top_ccu(self, unit_string):
        ''' Get the top (single) CCU representation (dictionary) for a given string. '''

        return self.get_all_ccu(unit_string)[0]

    def get_all_ccu(self, unit_string):
        ''' Get all the (multiple) CCU representations (ordered list of dictionaries) for a given string. '''

        return self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_string)

    def convert_ccu2ccu(self, ccu_src, ccu_dst, val_in):
        ''' Perfrom compound unit conversion for the given CCU representations. '''

        num_out, sts = self.ccut_inst.canonical_transform(ccu_src, ccu_dst, val_in)

        # remove metadata which we created during the transformation
        for cmp_unt in [ccu_src, ccu_dst]:
            for unt in cmp_unt['ccut:hasPart']:
                if '_metadata:total_dimension' in unt:
                    del unt['_metadata:total_dimension']

        return num_out, sts, RET_STR_MAP[sts]

    def convert_str2str(self, unit_src_string, unit_dst_string, val_in):
        ''' Perfrom compound unit conversion given the strings of the source and destination units. '''
        
        # get canonical representation
        ccu_src = self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_src_string)
        ccu_dst = self.ccut_inst.get_canonical_compound_unit_dict_from_string(unit_dst_string)
        
        num_out, sts, sts_str = self.convert_ccu2ccu(ccu_src[0], ccu_dst[0], val_in)
        return num_out, sts, sts_str, ccu_src[0], ccu_dst[0]