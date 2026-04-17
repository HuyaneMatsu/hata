import vampytest

from ..fields import put_primary_sku_id


def test__put_primary_sku_id():
    """
    Tests whether ``put_primary_sku_id`` is working as intended.
    """
    primary_sku_id = 202211270024
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'primary_sku_id': None}),
        (primary_sku_id, False, {'primary_sku_id': str(primary_sku_id)}),
    ):
        data = put_primary_sku_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
