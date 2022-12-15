import vampytest

from ..fields import validate_value


def test__validate_value__0():
    """
    Validates whether ``validate_value`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_value__1():
    """
    Validates whether ``validate_value`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_value(input_value)


def test__validate_value__2():
    """
    Validates whether ``validate_value`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_value(input_value)
