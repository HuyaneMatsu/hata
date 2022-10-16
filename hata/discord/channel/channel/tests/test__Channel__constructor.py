import vampytest

from ....core import CHANNELS

from ...message_history import MessageHistory

from ..channel import Channel
from ..channel_type import ChannelType
from ..metadata import ChannelMetadataBase
from ..utils import create_partial_channel_from_id


def _check_is_all_attribute_set(channel):
    """
    Checks whether all attributes of the channel is set.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    """
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_instance(channel.id, int)
    vampytest.assert_instance(channel._message_history, MessageHistory, nullable = True)
    vampytest.assert_instance(channel.guild_id, int)
    vampytest.assert_instance(channel.metadata, ChannelMetadataBase)
    vampytest.assert_instance(channel.type, ChannelType)
    


def test__Channel__new__0():
    """
    Tests whether ``Channel.__new__`` works as intended.
    
    Case: fields given.
    """
    channel_type = ChannelType.guild_text
    name = 'Rose'
    
    channel = Channel(channel_type = channel_type, name = name)
    _check_is_all_attribute_set(channel)
    
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.name, name)


def test__Channel__new__1():
    """
    Tests whether ``Channel.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel = Channel()
    _check_is_all_attribute_set(channel)


def test__Channel__precreate__0():
    """
    Tests whether ``Channel.precreate`` works as intended.
    
    Case: fields given.
    """
    channel_type = ChannelType.guild_text
    guild_id = 202209180131
    name = 'Rose'
    channel_id = 202209180132
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, guild_id = guild_id, name = name)
    _check_is_all_attribute_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)
    
    # Check cache too
    vampytest.assert_in(channel_id, CHANNELS)
    vampytest.assert_is(CHANNELS[channel_id], channel)


def test__Channel__precreate__1():
    """
    Tests whether ``Channel.precreate`` works as intended.
    
    Case: no fields given.
    """
    channel_id = 202209180133
    
    channel = Channel.precreate(channel_id)
    _check_is_all_attribute_set(channel)


def test__Channel__precreate__2():
    """
    Tests whether ``Channel.precreate`` works as intended.
    
    Case: already exists.
    """
    channel_id = 202209180133
    
    existing_channel = create_partial_channel_from_id(channel_id, ChannelType.unknown, 0)
    
    channel = Channel.precreate(channel_id)
    
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_is(channel, existing_channel)


def test__Channel__create_empty():
    """
    Tests whether ``Channel._create_empty`` works as intended.
    """
    channel_id = 202209180134
    channel_type = ChannelType.guild_text
    guild_id = 202209180135
    
    channel = Channel._create_empty(channel_id, channel_type, guild_id)
    _check_is_all_attribute_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.guild_id, guild_id)
    
    # This method should not cache
    vampytest.assert_not_in(channel_id, CHANNELS)


def test__Channel__create_private_data_less():
    """
    Tests whether ``Channel._create_private_data_less`` works as intended.
    """
    channel_id = 202209180138
    
    channel = Channel._create_private_data_less(channel_id)
    _check_is_all_attribute_set(channel)
    
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.type, ChannelType.private)
    
    # should cache too
    vampytest.assert_in(channel_id, CHANNELS)
    vampytest.assert_is(CHANNELS[channel_id], channel)
