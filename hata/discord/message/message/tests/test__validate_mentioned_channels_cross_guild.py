import vampytest

from ....channel import Channel

from ..fields import validate_mentioned_channels_cross_guild


def test__validate_mentioned_channels_cross_guild__0():
    """
    Validates whether ``validate_mentioned_channels_cross_guild`` works as intended.
    
    Case: passing.
    """
    channel_id_0 = 202304290000
    channel_id_1 = 202304290001
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    for input_value, expected_output in (
        ([], None),
        ([channel_0], (channel_0,)),
        ([channel_1, channel_0], (channel_0, channel_1)),
    ):
        output = validate_mentioned_channels_cross_guild(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_mentioned_channels_cross_guild__1():
    """
    Validates whether ``validate_mentioned_channels_cross_guild`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_mentioned_channels_cross_guild(input_value)
