import vampytest

from ..fields import parse_mute


def test__parse_mute():
    """
    Tests whether ``parse_mute`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'mute': False}, False),
        ({'mute': True}, True),
    ):
        output = parse_mute(input_data)
        vampytest.assert_eq(output, expected_output)
