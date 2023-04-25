import vampytest

from ....channel import Channel

from ..fields import validate_channel


def test__validate_channel__0():
    """
    Tests whether `validate_channel` works as intended.
    
    Case: passing.
    """
    channel_id = 202211010012
    channel = Channel.precreate(channel_id)
    
    for input_value, expected_output in (
        (channel, channel),
    ):
        output = validate_channel(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_channel__1():
    """
    Tests whether `validate_channel` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_channel(input_value)
