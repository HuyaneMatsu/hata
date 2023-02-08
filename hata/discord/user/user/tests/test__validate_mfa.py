import vampytest

from ..fields import validate_mfa


def test__validate_mfa__0():
    """
    Tests whether `validate_mfa` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_mfa(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_mfa__1():
    """
    Tests whether `validate_mfa` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_mfa(input_value)
