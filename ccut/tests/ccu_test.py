from ..main.ccut_main import CanonicalCompoundUnitTransformation_Main as ccut

def test():

    cc = ccut()

    for cmp_unt in ['kmi oz^2 / yr', 'kmi / oz^2', 'ft^3 kg']:
        top_ccu = cc.get_top_ccu(cmp_unt)
        all_ccu = cc.get_all_ccu(cmp_unt)
        assert top_ccu == all_ccu[0]