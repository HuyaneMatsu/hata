import vampytest

from ..fields import parse_boost_count


def test__parse_boost_count():
    """
    Tests whether ``parse_boost_count`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'premium_subscription_count': 1}, 1),
    ):
        output = parse_boost_count(input_data)
        vampytest.assert_eq(output, expected_output)
