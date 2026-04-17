import vampytest

from ..fields import parse_width


def test__parse_width():
    """
    Tests whether ``parse_width`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'width': 1}, 1),
    ):
        output = parse_width(input_data)
        vampytest.assert_eq(output, expected_output)
