import vampytest

from ..channel import Channel, ChannelType
from ..utils import create_partial_channel_data


def test__create_partial_channel_data():
    """
    Tests whether ``create_partial_channel_data`` works as intended.
    """
    channel_id = 202304280054
    guild_id = 202304280055
    name = 'Remilia'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
        name = name,
        channel_type = channel_type,
    )
    
    expected_output = {
        'id': str(channel_id),
        'guild_id': str(guild_id),
        'name': name,
        'type': channel_type.value,
    }
    
    vampytest.assert_eq(create_partial_channel_data(channel), expected_output)
