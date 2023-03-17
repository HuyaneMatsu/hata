import vampytest

from ..fields import validate_location


def test__validate_location__0():
    """
    Tests whether `validate_location` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_location(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_location__1():
    """
    Tests whether `validate_location` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_location(input_value)
