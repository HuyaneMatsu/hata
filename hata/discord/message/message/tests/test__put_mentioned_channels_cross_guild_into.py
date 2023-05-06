import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_mentioned_channels_cross_guild_into


def test__put_mentioned_channels_cross_guild_into__0():
    """
    Tests whether ``put_mentioned_channels_cross_guild_into`` works as intended.
    
    Case: non-empty.
    """
    guild_id = 202304280059
    
    channel_id_0 = 202304280060
    channel_id_1 = 202304280061
    name_0 = 'east'
    name_1 = 'new'
    channel_type_0 = ChannelType.guild_text
    channel_type_1 = ChannelType.guild_voice
    
    channel_0 = Channel.precreate(
        channel_id_0,
        name = name_0,
        channel_type = channel_type_0,
        guild_id = guild_id,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        name = name_1,
        channel_type = channel_type_1,
        guild_id = guild_id,
    )
    
    channels = (channel_0, channel_1)
    
    expected_output = {
        'mention_channels': [
            {
                'id': str(channel_id_0),
                'name': name_0,
                'type': channel_type_0.value,
                'guild_id': str(guild_id),
            }, {
                'id': str(channel_id_1),
                'name': name_1,
                'type': channel_type_1.value,
                'guild_id': str(guild_id),
            }
        ],
    }
    
    output = put_mentioned_channels_cross_guild_into(channels, {}, True)
    vampytest.assert_eq(output, expected_output)


def test__put_mentioned_channels_cross_guild_into__1():
    """
    Tests whether ``put_mentioned_channels_cross_guild_into`` works as intended.
    
    Case: empty.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'mention_channels': []}),
    ):
        output = put_mentioned_channels_cross_guild_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
