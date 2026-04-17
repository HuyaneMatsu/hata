import vampytest

from ..channel import Channel
from ..preinstanced import ChannelType
from ..utils import create_partial_channel_from_data


def test__create_partial_channel_from_data__new():
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
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)


def test__create_partial_channel_from_data__guild_id_in_data():
    """
    Tests whether ``create_partial_channel_from_data`` works as intended.
    
    Case: `guild_id` in data
    """
    channel_id = 202209180122
    guild_id = 202209180123
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
        'guild_id': str(guild_id),
    }
    
    channel = create_partial_channel_from_data(data)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)


def test__create_partial_channel_from_data__existing():
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


def test__create_partial_channel_from_data__caching():
    """
    Tests whether ``create_partial_channel_from_data`` works as intended.
    
    Case: caching.
    """
    channel_id = 202307300006
    guild_id = 202307300007
    
    data = {
        'id': str(channel_id),
    }
    
    channel_0 = create_partial_channel_from_data(data, guild_id)
    channel_1 = create_partial_channel_from_data(data, guild_id)
    
    vampytest.assert_is(channel_0, channel_1)
