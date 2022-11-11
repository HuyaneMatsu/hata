import vampytest

from ...color import Color

from ..fields import parse_color


def test__parse_color():
    """
    Tests whether ``parse_color`` works as intended."""
    for input_data, expected_output in (
        ({}, Color(0)),
        ({'color': 1}, Color(1)),
    ):
        output = parse_color(input_data)
        vampytest.assert_instance(output, Color)
        vampytest.assert_eq(output, expected_output)
