import vampytest

from ..fields import validate_height


def test__validate_height__0():
    """
    Tests whether `validate_height` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_height(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_height__1():
    """
    Tests whether `validate_height` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_height(input_value)


def test__validate_height__2():
    """
    Tests whether `validate_height` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_height(input_value)
