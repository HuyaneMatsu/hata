import vampytest

from ..fields import validate_image_small


def test__validate_image_small__0():
    """
    Tests whether `validate_image_small` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_image_small(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_image_small__1():
    """
    Tests whether `validate_image_small` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_image_small(input_value)
