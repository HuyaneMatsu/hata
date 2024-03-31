import vampytest

from ....channel import Channel, ChannelType

from ..guild import Guild

from ..fields import parse_channels


def _iter_options():
    channel_id = 202306080003
    channel_name = 'Koishi'
    
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield {}, {}
    yield {'channels': []}, {}
    yield (
        {'channels': [channel.to_data(defaults = True, include_internals = True)]},
        {channel_id: channel},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channels(input_value):
    """
    Tests whether ``parse_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    guild_id = 202306080004
    guild = Guild.precreate(guild_id)
    
    return parse_channels(input_value, guild.channels, guild_id)
