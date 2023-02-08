import vampytest

from ..fields import validate_access_token


def test__validate_access_token__0():
    """
    Tests whether `validate_access_token` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('aa', 'aa'),
    ):
        output = validate_access_token(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_access_token__1():
    """
    Tests whether `validate_access_token` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_access_token(input_value)
