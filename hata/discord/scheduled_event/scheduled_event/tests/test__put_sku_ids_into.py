import vampytest

from ..fields import put_sku_ids_into


def test__put_sku_ids_into():
    """
    Tests whether ``put_sku_ids_into`` is working as intended.
    """
    sku_id = 202303150008
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'sku_ids': []}),
        ((sku_id, ), False, {'sku_ids': [str(sku_id)]}),
    ):
        data = put_sku_ids_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
