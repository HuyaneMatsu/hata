import vampytest

from ..third_party_sku import ThirdPartySKU

from .test__ThirdPartySKU__constructor import _assert_is_every_attribute_set


def test__ThirdPartySKU__from_data():
    """
    Tests whether ``ThirdPartySKU.from_data`` works as intended.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    data = {
        'distributor': distributor,
        'id': id,
        'sku': sku,
    }
    
    third_party_sku = ThirdPartySKU.from_data(data)
    _assert_is_every_attribute_set(third_party_sku)
    
    vampytest.assert_eq(third_party_sku.distributor, distributor)
    vampytest.assert_eq(third_party_sku.id, id)
    vampytest.assert_eq(third_party_sku.sku, sku)


def test__ThirdPartySKU__to_data():
    """
    Tests whether ``ThirdPartySKU.to_data`` works as intended.
    
    Case: Include defaults.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    expected_output = {
        'distributor': distributor,
        'id': id,
        'sku': sku,
    }
    
    vampytest.assert_eq(third_party_sku.to_data(defaults = True), expected_output)
