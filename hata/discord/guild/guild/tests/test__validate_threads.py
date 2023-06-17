import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_threads


def test__validate_threads__0():
    """
    Tests whether ``validate_threads`` works as intended.
    
    Case: passing.
    """
    channel_id = 202306130027
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_thread_private,
        name = channel_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([channel], {channel_id: channel}),
        ({channel_id: channel}, {channel_id: channel}),
    ):
        output = validate_threads(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_threads__1():
    """
    Tests whether ``validate_threads`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_threads(input_value)
