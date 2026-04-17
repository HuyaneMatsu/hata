import vampytest

from ..fields import parse_boost_progress_bar_enabled


def test__parse_boost_progress_bar_enabled():
    """
    Tests whether ``parse_boost_progress_bar_enabled`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'premium_progress_bar_enabled': False}, False),
        ({'premium_progress_bar_enabled': True}, True),
    ):
        output = parse_boost_progress_bar_enabled(input_data)
        vampytest.assert_eq(output, expected_output)
