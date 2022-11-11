import vampytest

from ..fields import parse_focused


def test__parse_focused():
    """
    Tests whether ``parse_focused`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'focused': False}, False),
        ({'focused': True}, True),
    ):
        output = parse_focused(input_data)
        vampytest.assert_eq(output, expected_output)
