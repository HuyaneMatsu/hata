import vampytest

from ..fields import validate_secret


def test__validate_secret__0():
    """
    Tests whether `validate_secret` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        ('', ''),
        ('a', 'a'),
    ):
        output = validate_secret(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_secret__1():
    """
    Tests whether `validate_secret` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        None,
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_secret(input_value)
