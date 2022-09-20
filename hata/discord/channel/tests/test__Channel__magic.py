import vampytest

from ..channel import Channel
from ..channel_type import ChannelType


def test__Channel__repr():
    """
    Tests whether ``Channel.__repr__` works as intended.
    """
    channel_id = 202209180138
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(channel_id, name = name, channel_type = channel_type)
    
    vampytest.assert_instance(repr(channel), str)


def test__Channel__hash__0():
    """
    Tests whether ``Channel.__hash__` works as intended.
    
    Case: full channel.
    """
    channel_id = 202209180139
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(channel_id, name = name, channel_type = channel_type)
    
    vampytest.assert_instance(hash(channel), int)


def test__Channel__hash__1():
    """
    Tests whether ``Channel.__hash__` works as intended.
    
    Case: partial channel.
    """
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    channel = Channel(channel_type, name = name)
    
    vampytest.assert_instance(hash(channel), int)


def test__Channel__eq():
    """
    Tests whether ``Channel.__eq__` works as intended.
    """
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    guild_id = 202209180140
    channel_id_1 = 202209180141
    channel_id_2 = 202209180142
    
    keyword_parameters = {
        'channel_type': channel_type,
        'name': name,
    }
    
    channel = Channel.precreate(channel_id_1, **keyword_parameters, guild_id = guild_id)
    
    vampytest.assert_eq(channel, channel)
    vampytest.assert_ne(channel, object())
    
    # another full
    test_channel = Channel.precreate(channel_id_2, **keyword_parameters, guild_id = guild_id)
    vampytest.assert_ne(channel, test_channel)
    
    
    # partial
    test_channel = Channel(**keyword_parameters)
    vampytest.assert_eq(channel, test_channel)
    
    # different partials
    for field_name, field_value in (
        ('name', 'dread'),
        ('channel_type', ChannelType.guild_voice)
    ):
        test_channel = Channel(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(channel, test_channel)


def test__Channel__sort():
    """
    Tests whether sorting channels works.
    """
    channel_id_1 = 202209180144
    position_1 = 0
    channel_type_1 = ChannelType.guild_voice
    
    channel_id_2 = 202209180145
    position_2 = 0
    channel_type_2 = ChannelType.guild_voice
    
    channel_id_3 = 202209180146
    position_3 = 2
    channel_type_3 = ChannelType.guild_text
    
    channel_1 = Channel.precreate(channel_id_1, channel_type = channel_type_1, position = position_1)
    channel_2 = Channel.precreate(channel_id_2, channel_type = channel_type_2, position = position_2)
    channel_3 = Channel.precreate(channel_id_3, channel_type = channel_type_3, position = position_3)
    
    to_sort = [channel_2, channel_1, channel_3]
    to_sort.sort()
    
    vampytest.assert_eq(
        to_sort,
        [channel_3, channel_1, channel_2]
    )


def test__channel__format():
    """
    Tests whether ``Channel.__format__`` works as intended.
    """
    channel_id = 202209200019
    channel = Channel.precreate(channel_id)
    
    for format_code in ('', 'm', 'd', 'c'):
        string = format(channel, format_code)
        
        vampytest.assert_instance(string, str)
