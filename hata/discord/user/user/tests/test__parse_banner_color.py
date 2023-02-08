import vampytest

from ....color import Color

from ..fields import parse_banner_color


def test__parse_banner_color():
    """
    Tests whether ``parse_banner_color`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'accent_color': None}, None),
        ({'accent_color': 1}, 1),
    ):
        output = parse_banner_color(input_data)
        vampytest.assert_instance(output, Color, nullable = True)
        vampytest.assert_eq(output, expected_output)
