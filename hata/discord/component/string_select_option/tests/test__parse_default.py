import vampytest

from ..fields import parse_default


def test__parse_default():
    """
    Tests whether ``parse_default`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'default': False}, False),
        ({'default': True}, True),
    ):
        output = parse_default(input_data)
        vampytest.assert_eq(output, expected_output)
