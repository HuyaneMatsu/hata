import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channel_into


def test__put_channel_into():
    """
    Tests whether ``put_channel_into`` works as intended.
    """
    channel_id = 202212230002
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, name = 'Hotaru')
    
    for input_value, defaults, expected_output in (
        (channel, False, {'channel': channel.to_data(defaults = False, include_internals = True)}),
        (channel, True, {'channel': channel.to_data(defaults = True, include_internals = True)}),
    ):
        data = put_channel_into(input_value, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
