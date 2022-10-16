import vampytest

from ..position import validate_position


def test__validate_position__0():
    """
    Tests whether `validate_position` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_position(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_position__1():
    """
    Tests whether `validate_position` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_position(input_value)


def test__validate_position__2():
    """
    Tests whether `validate_position` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_position(input_value)
