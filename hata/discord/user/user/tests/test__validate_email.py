import vampytest

from ..fields import validate_email


def test__validate_email__0():
    """
    Tests whether `validate_email` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('meow', 'meow'),
    ):
        output = validate_email(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_email__1():
    """
    Tests whether `validate_email` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_email(input_value)
