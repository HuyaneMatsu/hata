import vampytest

from ..constants import (
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN,
    APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX
)
from ..fields import validate_min_length
from ..preinstanced import ApplicationCommandOptionType


def test__validate_min_length__0():
    """
    Tests whether `validate_min_length` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT),
        (APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT),
        (10, 10),
        (APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN - 10, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MIN),
        (APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX + 10, APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX),
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


def test__validate_min_length__2():
    """
    Tests whether `validate_min_length` works as intended.
    
    Case: `ValueError`.
    """
    with vampytest.assert_raises(ValueError):
        validate_min_length(10, ApplicationCommandOptionType.float)
