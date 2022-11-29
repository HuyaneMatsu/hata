import vampytest

from ..fields import parse_bot_public


def test__parse_bot_public():
    """
    Tests whether ``parse_bot_public`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'bot_public': False}, False),
        ({'bot_public': True}, True),
    ):
        output = parse_bot_public(input_data)
        vampytest.assert_eq(output, expected_output)
