import vampytest

from ....channel import Channel

from ..fields import parse_channel


def _iter_options():
    channel_id = 202307290000
    channel = Channel.precreate(channel_id)
    
    yield {}, None
    yield {'channel': None}, None
    yield {'channel': {'id': str(channel_id)}}, channel
    yield {'channel_id': None}, None
    yield {'channel_id': str(channel_id)}, channel


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channel(input_data):
    """
    Tests whether ``parse_channel`` works as intended.
    
    Parameters
    ----------
    input_data : `str`
        Data to parse from.
    
    Returns
    -------
    output : `None`, ``Channel``
    """
    return parse_channel(input_data)


def test__parse_channel__with_guild_id():
    """
    Tests whether ``parse_channel`` works as intended.
    
    Case: `guild_id` also given.
    """
    channel_id = 202307290001
    guild_id = 202307290002
    
    data = {'channel': {'id': str(channel_id)}}
    
    channel = parse_channel(data, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_eq(channel.guild_id, guild_id)
