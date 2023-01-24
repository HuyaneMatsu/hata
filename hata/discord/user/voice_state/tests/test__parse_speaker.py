import vampytest

from ..fields import parse_speaker


def test__parse_speaker():
    """
    Tests whether ``parse_speaker`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'suppress': True}, False),
        ({'suppress': False}, True),
    ):
        output = parse_speaker(input_data)
        vampytest.assert_eq(output, expected_output)
