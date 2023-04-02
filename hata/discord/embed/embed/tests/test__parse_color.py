import vampytest

from ....color import Color

from ..fields import parse_color


def test__parse_color():
    """
    Tests whether ``parse_color`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'color': None}, None),
        ({'color': 1}, Color(1)),
    ):
        output = parse_color(input_data)
        vampytest.assert_instance(output, Color, nullable = True)
        vampytest.assert_eq(output, expected_output)
