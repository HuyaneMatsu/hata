import vampytest

from ....channel import ChannelType

from ..fields import validate_channel_types


def test__validate_channel_types__0():
    """
    Tests whether `validate_channel_types` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([ChannelType.private], (ChannelType.private, )),
        ([ChannelType.private.value], (ChannelType.private, )),
    ):
        output = validate_channel_types(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_channel_types__1():
    """
    Tests whether `validate_channel_types` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_channel_types(input_value)
