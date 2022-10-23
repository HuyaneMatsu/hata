import vampytest

from ..fields import parse_enabled


def test__parse_enabled():
    """
    Tests whether ``parse_enabled`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'disabled': False}, True),
        ({'disabled': True}, False),
    ):
        output = parse_enabled(input_data)
        vampytest.assert_eq(output, expected_output)
