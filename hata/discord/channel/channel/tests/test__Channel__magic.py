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


def test__Channel__hash__full():
    """
    Tests whether ``Channel.__hash__` works as intended.
    
    Case: full channel.
    """
    channel_id = 202209180139
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(channel_id, name = name, channel_type = channel_type)
    
    vampytest.assert_instance(hash(channel), int)


def test__Channel__hash__partial():
    """
    Tests whether ``Channel.__hash__` works as intended.
    
    Case: partial channel.
    """
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    channel = Channel(channel_type = channel_type, name = name)
    
    vampytest.assert_instance(hash(channel), int)


def _iter_options__eq():
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    
    keyword_parameters = {
        'channel_type': channel_type,
        'name': name,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'dread',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_type': ChannelType.guild_voice,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Channel__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Channel.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    channel_0 = Channel(**keyword_parameters_0)
    channel_1 = Channel(**keyword_parameters_1)
    
    output = channel_0 == channel_1
    vampytest.assert_instance(output, bool)
    return output


def test__Channel__eq__partial__non_partial():
    """
    Tests whether ``Channel.__eq__` works as intended.
    
    Case: partial, non partial.
    """
    name = 'Frantic'
    channel_type = ChannelType.guild_text
    guild_id = 202209180140
    channel_id_0 = 202209180141
    channel_id_1 = 202209180142
    
    channel = Channel.precreate(channel_id_0, channel_type = channel_type, guild_id = guild_id, name = name)
    
    vampytest.assert_eq(channel, channel)
    vampytest.assert_ne(channel, object())
    
    # another full
    test_channel = Channel.precreate(channel_id_1, channel_type = channel_type, guild_id = guild_id, name = name)
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
