import vampytest

from ....color import Color

from ..fields import validate_banner_color


def test__validate_banner_color__0():
    """
    Tests whether `validate_banner_color` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, Color(1)),
        (Color(1), Color(1)),
        (None, None),
    ):
        output = validate_banner_color(input_value)
        vampytest.assert_instance(output, Color, nullable = True)
        vampytest.assert_eq(output, expected_output)


def test__validate_banner_color__1():
    """
    Tests whether `validate_banner_color` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_banner_color(input_value)


def test__validate_banner_color__2():
    """
    Tests whether `validate_banner_color` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
        999999999,
    ):
        with vampytest.assert_raises(ValueError):
            validate_banner_color(input_value)
