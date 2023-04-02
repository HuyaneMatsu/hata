import vampytest

from ....color import Color

from ..fields import validate_color


def test__validate_color__0():
    """
    Tests whether `validate_color` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        (1, Color(1)),
        (Color(1), Color(1)),
    ):
        output = validate_color(input_value)
        vampytest.assert_instance(output, Color, nullable = True)
        vampytest.assert_eq(output, expected_output)


def test__validate_color__1():
    """
    Tests whether `validate_color` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_color(input_value)
