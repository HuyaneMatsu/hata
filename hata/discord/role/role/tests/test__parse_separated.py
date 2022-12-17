import vampytest

from ..fields import parse_separated


def test__parse_separated():
    """
    Tests whether ``parse_separated`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'hoist': False}, False),
        ({'hoist': True}, True),
    ):
        output = parse_separated(input_data)
        vampytest.assert_eq(output, expected_output)
