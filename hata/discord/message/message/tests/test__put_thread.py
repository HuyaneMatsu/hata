import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_thread


def test__put_thread():
    """
    Tests whether ``put_thread`` works as intended.
    """
    channel = Channel.precreate(
        202304300015,
        name = 'More ENS',
        channel_type = ChannelType.guild_thread_private,
        guild_id = 202304300016,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'thread': None}),
        (channel, False, {'thread': channel.to_data(include_internals = True)}),
        (channel, True, {'thread': channel.to_data(defaults = True, include_internals = True)}),
    ):
        output = put_thread(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
