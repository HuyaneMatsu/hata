import vampytest

from ..fields import validate_user_limit


def test__validate_user_limit__0():
    """
    Validates whether ``validate_user_limit`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
    ):
        output = validate_user_limit(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_user_limit__1():
    """
    Validates whether ``validate_user_limit`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_user_limit(input_value)


def test__validate_user_limit__2():
    """
    Validates whether ``validate_user_limit`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_user_limit(input_value)
