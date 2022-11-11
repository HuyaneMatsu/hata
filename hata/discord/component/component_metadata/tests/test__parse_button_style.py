import vampytest

from ..preinstanced import ButtonStyle

from ..fields import parse_button_style


def test__parse_button_style():
    """
    Tests whether ``parse_button_style`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ButtonStyle.blue),
        ({'style': ButtonStyle.blue.value}, ButtonStyle.blue),
        ({'style': ButtonStyle.red.value}, ButtonStyle.red),
    ):
        output = parse_button_style(input_data)
        vampytest.assert_eq(output, expected_output)
