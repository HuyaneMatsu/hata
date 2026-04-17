import vampytest

from ..constants import MIN_LENGTH_DEFAULT, MIN_LENGTH_MIN, MIN_LENGTH_MAX
from ..fields import validate_min_length


def test__validate_min_length__0():
    """
    Tests whether `validate_min_length` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, MIN_LENGTH_DEFAULT),
        (MIN_LENGTH_DEFAULT, MIN_LENGTH_DEFAULT),
        (10, 10),
        (MIN_LENGTH_MIN - 10, MIN_LENGTH_MIN),
        (MIN_LENGTH_MAX + 10, MIN_LENGTH_MAX),
    ):
        output = validate_min_length(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_min_length__1():
    """
    Tests whether `validate_min_length` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_min_length(input_value)
