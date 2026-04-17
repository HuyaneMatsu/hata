import vampytest

from ..constants import (
    MAX_LENGTH_DEFAULT, MAX_LENGTH_MIN,
    MAX_LENGTH_MAX
)
from ..fields import validate_max_length


def test__validate_max_length__0():
    """
    Tests whether `validate_max_length` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, MAX_LENGTH_DEFAULT),
        (MAX_LENGTH_DEFAULT, MAX_LENGTH_DEFAULT),
        (10, 10),
        (MAX_LENGTH_MIN - 10, MAX_LENGTH_MIN),
        (MAX_LENGTH_MAX + 10, MAX_LENGTH_DEFAULT),
    ):
        output = validate_max_length(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_length__1():
    """
    Tests whether `validate_max_length` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_length(input_value)
