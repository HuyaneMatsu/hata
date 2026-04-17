import vampytest

from ..fields import parse_primary_sku_id


def test__parse_primary_sku_id():
    """
    Tests whether ``parse_primary_sku_id`` works as intended.
    """
    primary_sku_id = 202211270023
    
    for input_data, expected_output in (
        ({}, 0),
        ({'primary_sku_id': None}, 0),
        ({'primary_sku_id': str(primary_sku_id)}, primary_sku_id),
    ):
        output = parse_primary_sku_id(input_data)
        vampytest.assert_eq(output, expected_output)
