import vampytest

from ...core import CHANNELS

from ..channel import Channel
from ..channel_type import ChannelType
from ..utils import create_partial_channel_from_data


def test__create_partial_channel_from_data__0():
    """
    Tests whether ``create_partial_channel_from_data`` works as intended.
    
    Case: creating new channel.
    """
    channel_id = 202209180120
    guild_id = 202209180121
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    channel = create_partial_channel_from_data(data, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_in(channel_id, CHANNELS)
    vampytest.assert_is(CHANNELS[channel_id], channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)


def test__create_partial_channel_from_data__1():
    """
    Tests whether ``create_partial_channel_from_data`` works as intended.
    
    Case: empty data.
    """
    guild_id = 202209180122
    
    for data in (
        None,
        {},
    ):
        channel = create_partial_channel_from_data(data, guild_id)
        
        vampytest.assert_is(channel, None)


def test__create_partial_channel_from_data__2():
    """
    Tests whether ``create_partial_channel_from_data`` works as intended.
    
    Case: channel already exists.
    """
    channel_id = 202209180124
    guild_id = 202209180123
    
    existing_channel = Channel.precreate(channel_id)
    
    data = {
        'id': str(channel_id),
    }
    
    channel = create_partial_channel_from_data(data, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_is(channel, existing_channel)
