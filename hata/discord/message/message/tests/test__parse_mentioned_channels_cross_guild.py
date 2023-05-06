import vampytest

from ....channel import Channel, ChannelType

from ..fields import parse_mentioned_channels_cross_guild


def test__parse_mentioned_channels_cross_guild__0():
    """
    Tests whether ``parse_mentioned_channels_cross_guild`` works as intended.
    
    Case: non-empty.
    """
    guild_id = 202304280058
    
    channel_id_0 = 202304280056
    channel_id_1 = 202304280057
    name_0 = 'east'
    name_1 = 'new'
    channel_type_0 = ChannelType.guild_text
    channel_type_1 = ChannelType.guild_voice
    
    data = {
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
    
    output = parse_mentioned_channels_cross_guild(data)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    vampytest.assert_instance(output[0], Channel)
    vampytest.assert_eq(output[0].id, channel_id_0)
    vampytest.assert_is(output[0].type, channel_type_0)
    vampytest.assert_eq(output[0].guild_id, guild_id)
    vampytest.assert_eq(output[0].name, name_0)

    vampytest.assert_instance(output[1], Channel)
    vampytest.assert_eq(output[1].id, channel_id_1)
    vampytest.assert_is(output[1].type, channel_type_1)
    vampytest.assert_eq(output[1].guild_id, guild_id)
    vampytest.assert_eq(output[1].name, name_1)


def test__parse_mentioned_channels_cross_guild__1():
    """
    Tests whether ``parse_mentioned_channels_cross_guild`` works as intended.
    
    Case: empty.
    """
    for input_data in (
        {},
        {'mention_channels': None},
        {'mention_channels': []},
    ):
        output = parse_mentioned_channels_cross_guild(input_data)
        
        vampytest.assert_is(output, None)
