import vampytest

from ..fields import validate_match


def test__validate_match__0():
    """
    Tests whether `validate_match` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_match(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_match__1():
    """
    Tests whether `validate_match` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_match(input_value)
