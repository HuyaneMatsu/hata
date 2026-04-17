import vampytest

from ..fields import parse_purchasable


def test__parse_purchasable():
    """
    Tests whether ``parse_purchasable`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'available_for_purchase': None}, True),
    ):
        output = parse_purchasable(input_data)
        vampytest.assert_eq(output, expected_output)
