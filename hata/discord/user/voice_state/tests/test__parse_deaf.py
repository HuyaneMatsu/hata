import vampytest

from ..fields import parse_deaf


def test__parse_deaf():
    """
    Tests whether ``parse_deaf`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'deaf': False}, False),
        ({'deaf': True}, True),
    ):
        output = parse_deaf(input_data)
        vampytest.assert_eq(output, expected_output)
