import vampytest

from ..fields import validate_duration


def test__validate_duration__0():
    """
    Tests whether `validate_duration` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
        (12.6, 13),
        (None, 0),
    ):
        output = validate_duration(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_duration__1():
    """
    Tests whether `validate_duration` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'hello',
    ):
        with vampytest.assert_raises(TypeError):
            validate_duration(input_value)
