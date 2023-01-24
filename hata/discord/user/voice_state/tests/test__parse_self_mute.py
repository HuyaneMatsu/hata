import vampytest

from ..fields import parse_self_mute


def test__parse_self_mute():
    """
    Tests whether ``parse_self_mute`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'self_mute': False}, False),
        ({'self_mute': True}, True),
    ):
        output = parse_self_mute(input_data)
        vampytest.assert_eq(output, expected_output)
