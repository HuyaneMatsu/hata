import vampytest

from ..constants import (
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN,
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX
)
from ..fields import validate_max_length
from ..preinstanced import ApplicationCommandOptionType


def test__validate_max_length__0():
    """
    Tests whether `validate_max_length` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
        (APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
        (10, 10),
        (APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN - 10, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MIN),
        (APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX + 10, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
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


def test__validate_max_length__2():
    """
    Tests whether `validate_max_length` works as intended.
    
    Case: `ValueError`.
    """
    with vampytest.assert_raises(ValueError):
        validate_max_length(10, ApplicationCommandOptionType.float)
