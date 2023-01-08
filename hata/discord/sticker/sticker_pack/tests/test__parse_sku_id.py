import vampytest

from ..fields import parse_sku_id


def test__parse_sku_id():
    """
    Tests whether ``parse_sku_id`` works as intended.
    """
    sku_id = 202301050011
    
    for input_data, expected_output in (
        ({}, 0),
        ({'sku_id': None}, 0),
        ({'sku_id': str(sku_id)}, sku_id),
    ):
        output = parse_sku_id(input_data)
        vampytest.assert_eq(output, expected_output)
