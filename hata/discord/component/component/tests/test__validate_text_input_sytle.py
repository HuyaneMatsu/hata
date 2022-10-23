import vampytest

from ..fields import validate_text_input_style
from ..preinstanced import TextInputStyle


def test__validate_text_input_style__0():
    """
    Tests whether `validate_text_input_style` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (TextInputStyle.short, TextInputStyle.short),
        (TextInputStyle.paragraph.value, TextInputStyle.paragraph)
    ):
        output = validate_text_input_style(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_text_input_style__1():
    """
    Tests whether `validate_text_input_style` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_text_input_style(input_value)
