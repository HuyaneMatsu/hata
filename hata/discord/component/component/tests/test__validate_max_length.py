import vampytest

from ..fields import validate_max_length


def test__validate_max_length__0():
    """
    Validates whether ``validate_max_length`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_max_length(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_length__1():
    """
    Validates whether ``validate_max_length`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_length(input_value)


def test__validate_max_length__2():
    """
    Validates whether ``validate_max_length`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_length(input_value)
