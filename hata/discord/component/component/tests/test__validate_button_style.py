import vampytest

from ..fields import validate_button_style
from ..preinstanced import ButtonStyle


def test__validate_button_style__0():
    """
    Tests whether `validate_button_style` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ButtonStyle.red, ButtonStyle.red),
        (ButtonStyle.red.value, ButtonStyle.red)
    ):
        output = validate_button_style(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_button_style__1():
    """
    Tests whether `validate_button_style` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_button_style(input_value)
