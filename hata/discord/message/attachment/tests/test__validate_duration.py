import vampytest

from ..fields import validate_duration


def test__validate_duration__0():
    """
    Tests whether `validate_duration` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1.0, 1.0),
        (12.6, 12.6),
    ):
        output = validate_duration(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_duration__1():
    """
    Tests whether `validate_duration` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1.0,
    ):
        with vampytest.assert_raises(ValueError):
            validate_duration(input_value)


def test__validate_duration__2():
    """
    Tests whether `validate_duration` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'senya',
    ):
        with vampytest.assert_raises(TypeError):
            validate_duration(input_value)
