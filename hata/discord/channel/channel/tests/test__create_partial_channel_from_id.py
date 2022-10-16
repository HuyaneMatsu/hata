import vampytest

from ....core import CHANNELS

from ..channel import Channel
from ..channel_type import ChannelType
from ..utils import create_partial_channel_from_id


def test__create_partial_channel_from_id__0():
    """
    Tests whether ``create_partial_channel_from_id`` works as intended.
    
    Case: New channel.
    """
    channel_id = 202209180125
    channel_type = ChannelType.unknown
    guild_id = 202209180126
    
    channel = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_in(channel_id, CHANNELS)
    vampytest.assert_is(CHANNELS[channel_id], channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)


def test__create_partial_channel_from_id__1():
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
