import vampytest

from ..fields import validate_min_values


def test__validate_min_values__0():
    """
    Validates whether ``validate_min_values`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_min_values(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_min_values__1():
    """
    Validates whether ``validate_min_values`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_min_values(input_value)


def test__validate_min_values__2():
    """
    Validates whether ``validate_min_values`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_min_values(input_value)
