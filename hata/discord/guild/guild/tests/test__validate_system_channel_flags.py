import vampytest

from ..fields import validate_system_channel_flags
from ..flags import SystemChannelFlag


def test__validate_system_channel_flags__0():
    """
    Tests whether `validate_system_channel_flags` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, SystemChannelFlag.NONE),
        (1, SystemChannelFlag(1)),
        (SystemChannelFlag(1), SystemChannelFlag(1)),
    ):
        output = validate_system_channel_flags(input_value)
        vampytest.assert_instance(output, SystemChannelFlag)
        vampytest.assert_eq(output, expected_output)


def test__validate_system_channel_flags__1():
    """
    Tests whether `validate_system_channel_flags` works as intended.
    
    Case: type error
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_system_channel_flags(input_value)
