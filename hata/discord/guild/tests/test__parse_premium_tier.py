import vampytest

from ..fields import parse_premium_tier


def test__parse_premium_tier():
    """
    Tests whether ``parse_premium_tier`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'premium_tier': 1}, 1),
    ):
        output = parse_premium_tier(input_data)
        vampytest.assert_eq(output, expected_output)
