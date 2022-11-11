import vampytest

from ..preinstanced import TextInputStyle

from ..fields import parse_text_input_style


def test__parse_text_input_style():
    """
    Tests whether ``parse_text_input_style`` works as intended.
    """
    for input_data, expected_output in (
        ({}, TextInputStyle.short),
        ({'style': TextInputStyle.short.value}, TextInputStyle.short),
        ({'style': TextInputStyle.paragraph.value}, TextInputStyle.paragraph),
    ):
        output = parse_text_input_style(input_data)
        vampytest.assert_eq(output, expected_output)
