import vampytest

from ..fields import validate_slowmode


def test__validate_slowmode__0():
    """
    Validates whether ``validate_slowmode`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
    ):
        output = validate_slowmode(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_slowmode__1():
    """
    Validates whether ``validate_slowmode`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_slowmode(input_value)



def test__validate_slowmode__2():
    """
    Validates whether ``validate_slowmode`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_slowmode(input_value)
