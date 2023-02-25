import vampytest

from ..preinstanced import ApplicationCommandOptionType
from ..fields import validate_max_value


def test__validate_max_value__0():
    """
    Tests whether `validate_max_value` works as intended.
    
    Case: passing.
    """
    for input_value, input_option_type, expected_output in (
        (None, ApplicationCommandOptionType.channel, None),
        (10, ApplicationCommandOptionType.none, 10),
        (10, ApplicationCommandOptionType.integer, 10),
        (10.0, ApplicationCommandOptionType.none, 10.0),
        (10.0, ApplicationCommandOptionType.float, 10.0),
    ):
        output = validate_max_value(input_value, input_option_type)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_value__1():
    """
    Tests whether `validate_max_value` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'pepe',
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_value(input_value)


def test__validate_max_value__2():
    """
    Tests whether `validate_max_value` works as intended.
    
    Case: `ValueError`.
    """
    for input_value, input_option_type in (
        (10.0, ApplicationCommandOptionType.integer),
        (10, ApplicationCommandOptionType.float),
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_value(input_value, input_option_type)
