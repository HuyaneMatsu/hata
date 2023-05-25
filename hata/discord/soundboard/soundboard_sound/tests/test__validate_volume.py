import vampytest

from ..fields import validate_volume


def test__validate_volume__0():
    """
    Tests whether `validate_volume` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1.0, 1.0),
        (0.0, 0.0),
        (0.5, 0.5),
    ):
        output = validate_volume(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_volume__1():
    """
    Tests whether `validate_volume` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1.0,
        +2.0,
    ):
        with vampytest.assert_raises(ValueError):
            validate_volume(input_value)


def test__validate_volume__2():
    """
    Tests whether `validate_volume` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'senya',
    ):
        with vampytest.assert_raises(TypeError):
            validate_volume(input_value)
