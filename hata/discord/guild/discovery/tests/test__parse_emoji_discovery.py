import vampytest

from ..fields import parse_emoji_discovery


def test__parse_emoji_discovery():
    """
    Tests whether ``parse_emoji_discovery`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'emoji_discoverability_enabled': False}, False),
        ({'emoji_discoverability_enabled': True}, True),
    ):
        output = parse_emoji_discovery(input_data)
        vampytest.assert_eq(output, expected_output)
