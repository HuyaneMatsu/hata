import vampytest

from ..third_party_sku import ThirdPartySKU


def test__ThirdPartySKU__repr():
    """
    Tests whether ``ThirdPartySKU.__repr__`` works as intended.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    vampytest.assert_instance(repr(third_party_sku), str)


def test__ThirdPartySKU__hash():
    """
    Tests whether ``ThirdPartySKU.__hash__`` works as intended.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    third_party_sku = ThirdPartySKU(
        distributor = distributor,
        sku_id = id,
        sku = sku,
    )
    
    vampytest.assert_instance(hash(third_party_sku), int)


def test__ThirdPartySKU__eq():
    """
    Tests whether ``ThirdPartySKU.__eq__`` works as intended.
    """
    distributor = 'RECORDS'
    id = 'WARNING'
    sku = 'NJK'
    
    keyword_sku = {
        'distributor': distributor,
        'sku_id': id,
        'sku': sku,
    }
    
    third_party_sku = ThirdPartySKU(**keyword_sku)
    vampytest.assert_eq(third_party_sku, third_party_sku)
    vampytest.assert_ne(third_party_sku, object())
    
    for field_id, field_value in (
        ('distributor', 'Orin'),
        ('sku_id', 'okuu'),
        ('sku', 'dance')
    ):
        test_third_party_sku = ThirdPartySKU(**{**keyword_sku, field_id: field_value})
        vampytest.assert_ne(third_party_sku, test_third_party_sku)



def test__ThirdPartySKU__sort():
    """
    Tests whether ``ThirdPartySKU`` sorting works.
    """
    third_party_sku_0 = ThirdPartySKU(
        distributor = 'RECORDS',
        sku_id = 'WARNING',
        sku = 'NJK',
    )
    
    third_party_sku_1 = ThirdPartySKU(
        distributor = 'Suika',
        sku_id = 'WARNING',
        sku = 'NJK',
    )
    
    vampytest.assert_eq(
        sorted([third_party_sku_1, third_party_sku_0]),
        [third_party_sku_0, third_party_sku_1],
    )
