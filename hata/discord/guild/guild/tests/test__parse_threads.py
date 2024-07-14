import vampytest

from ....channel import Channel, ChannelType

from ..guild import Guild

from ..fields import parse_threads


def _iter_options():
    channel_id = 202306130024
    channel_name = 'Koishi'
    
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_thread_public,
        name = channel_name,
    )
    
    yield {}, None
    yield {'threads': []}, None
    yield (
        {'threads': [channel.to_data(defaults = True, include_internals = True)]},
        {channel_id: channel},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_threads(input_value):
    """
    Tests whether ``parse_threads`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    Returns
    -------
    output : `None | dict<int, Channel>`
    """
    guild_id = 202306130025
    guild = Guild.precreate(guild_id)
    
    return parse_threads(input_value, guild.threads, guild_id)
