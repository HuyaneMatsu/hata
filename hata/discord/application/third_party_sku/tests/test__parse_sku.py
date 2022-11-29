import vampytest

from ..fields import parse_sku


def test__parse_sku():
    """
    Tests whether ``parse_sku`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'sku': None}, ''),
        ({'sku': ''}, ''),
        ({'sku': 'a'}, 'a'),
    ):
        output = parse_sku(input_data)
        vampytest.assert_eq(output, expected_output)
