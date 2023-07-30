import vampytest

from ..channel import Channel
from ..preinstanced import ChannelType
from ..utils import create_partial_channel_from_id


def test__create_partial_channel_from_id__new():
    """
    Tests whether ``create_partial_channel_from_id`` works as intended.
    
    Case: New channel.
    """
    channel_id = 202209180125
    channel_type = ChannelType.guild_text
    guild_id = 202209180126
    
    channel = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.guild_id, guild_id)


def test__create_partial_channel_from_id__existing():
    """
    Tests whether ``create_partial_channel_from_id`` works as intended.
    
    Case: existing channel.
    """
    channel_id = 202209180127
    channel_type = ChannelType.unknown
    guild_id = 202209180128
    
    existing_channel = Channel.precreate(channel_id)
    
    channel = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_is(channel, existing_channel)


def test__create_partial_channel_from_id__caching():
    
    """
    Tests whether ``create_partial_channel_from_id`` works as intended.
    
    Case: existing channel.
    """
    channel_id = 202307300001
    channel_type = ChannelType.unknown
    guild_id = 202307300002
    
    channel_0 = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    channel_1 = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    
    vampytest.assert_is(channel_0, channel_1)
