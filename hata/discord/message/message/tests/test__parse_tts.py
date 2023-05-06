import vampytest

from ..fields import parse_tts


def test__parse_tts():
    """
    Tests whether ``parse_tts`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'tts': False}, False),
        ({'tts': True}, True),
    ):
        output = parse_tts(input_data)
        vampytest.assert_eq(output, expected_output)
