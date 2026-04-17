import vampytest

from ..third_party_sku import ThirdPartySKU


def _assert_fields_set(third_party_sku):
    """
    Asserts whether every attributes are set of the given sku.
    
    Parameters
    ----------
    third_party_sku : ``ThirdPartySKU``
    """
    vampytest.assert_instance(third_party_sku, ThirdPartySKU)
    vampytest.assert_instance(third_party_sku.distributor, str)
    vampytest.assert_instance(third_party_sku.id, str)
    vampytest.assert_instance(third_party_sku.sku, str)



def test__ThirdPartySKU__new__0():
    """
    Tests whether ``ThirdPartySKU.__new__`` works as intended.
    
    Case: No sku.
    """
    third_party_sku = ThirdPartySKU()
    _assert_fields_set(third_party_sku)


def test__ThirdPartySKU__new__1():
    """
    Tests whether ``ThirdPartySKU.__new__`` works as intended.
    
    Case: Give all sku.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    _assert_fields_set(third_party_sku)
    vampytest.assert_eq(third_party_sku.distributor, distributor)
    vampytest.assert_eq(third_party_sku.id, id)
    vampytest.assert_eq(third_party_sku.sku, sku)
