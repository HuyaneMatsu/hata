import vampytest

from ..third_party_sku import ThirdPartySKU

from .test__ThirdPartySKU__constructor import _assert_is_every_attribute_set


def test__ThirdPartySKU__copy():
    """
    Tests whether ``ThirdPartySKU.copy`` works as intended.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    copy = third_party_sku.copy()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(third_party_sku, copy)
    vampytest.assert_is_not(third_party_sku, copy)


def test__ThirdPartySKU__copy_with__0():
    """
    Tests whether ``ThirdPartySKU.copy`` works as intended.
    
    Case: No sku
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    copy = third_party_sku.copy_with()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(third_party_sku, copy)
    vampytest.assert_is_not(third_party_sku, copy)


def test__ThirdPartySKU__copy_with__1():
    """
    Tests whether ``ThirdPartySKU.copy`` works as intended.
    
    Case: No sku
    """
    old_distributor = 'RECORDS'
    new_distributor = 'Orin'
    old_id = 'WARNING'
    new_id = 'Okuu'
    old_sku = 'NJK'
    new_sku = 'dance'
    
    third_party_sku = ThirdPartySKU(
        distributor = old_distributor,
        sku_id = old_id,
        sku = old_sku,
    )
    
    copy = third_party_sku.copy_with(
        distributor = new_distributor,
        sku_id = new_id,
        sku = new_sku,
    )
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(third_party_sku, copy)

    vampytest.assert_eq(copy.distributor, new_distributor)
    vampytest.assert_eq(copy.id, new_id)
    vampytest.assert_eq(copy.sku, new_sku)
