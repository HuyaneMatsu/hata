import vampytest

from ....channel import Channel, ChannelType

from ..fields import parse_threads


def _iter_options():
    guild_id = 2024062400012
    channel_id_0 = 2024062400010
    channel_id_1 = 2024062400011
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'threads': [],
        },
        None,
    )
    
    yield (
        {
            'threads': [
                channel_0.to_data(defaults = True, include_internals = True),
                channel_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            channel_id_0: channel_0,
            channel_id_1: channel_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_threads(input_data):
    """
    Tests whether ``parse_threads`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, Channel>`
    """
    return parse_threads(input_data)
