import vampytest

from ..fields import parse_total_months


def test__parse_total_months():
    """
    Tests whether ``parse_total_months`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 1),
        ({'total_months_subscribed': 2}, 2),
    ):
        output = parse_total_months(input_data)
        vampytest.assert_eq(output, expected_output)
