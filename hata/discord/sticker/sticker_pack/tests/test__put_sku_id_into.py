import vampytest

from ..fields import put_sku_id_into


def test__put_sku_id_into():
    """
    Tests whether ``put_sku_id_into`` works as intended.
    """
    sku_id = 202301040012
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'sku_id': None}),
        (sku_id, False, {'sku_id': str(sku_id)}),
    ):
        output = put_sku_id_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
