import vampytest

from ..channel import Channel
from ..preinstanced import ChannelType


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
    
    channel = Channel(channel_type = channel_type, name = name)
    
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
    channel_0 = Channel.precreate(202209180144, channel_type = ChannelType.guild_voice, position = 0)
    channel_1 = Channel.precreate(202209180145, channel_type = ChannelType.guild_voice, position = 0)
    channel_2 = Channel.precreate(202209180146, channel_type = ChannelType.guild_text, position = 2)
    channel_3 = Channel.precreate(202306270080, channel_type = ChannelType.guild_category, position = 4)
    channel_4 = Channel.precreate(202306270081, channel_type = ChannelType.guild_category, position = 0)
    
    to_sort = [channel_0, channel_1, channel_2, channel_3, channel_4]
    to_sort.sort()
    
    vampytest.assert_eq(
        to_sort,
        [channel_2, channel_0, channel_1, channel_4, channel_3]
    )


@vampytest.call_from(['', 'm', 'd', 'c'])
def test__Channel__format__passing(format_code):
    """
    Tests whether ``Channel.__format__`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    format_code : `str`
        The format code to test.
    """
    channel = Channel()
    
    output = format(channel, format_code)
    vampytest.assert_instance(output, str)


@vampytest.raising(ValueError)
@vampytest.call_from(['_', 'm_', 'dd', '_c'])
def test__Channel__format__failing(format_code):
    """
    Tests whether ``Channel.__format__`` works as intended.
    
    Case: failing.
    
    Parameters
    ----------
    format_code : `str`
        The format code to test.
    """
    channel = Channel()
    
    format(channel, format_code)
