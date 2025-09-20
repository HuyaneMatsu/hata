import vampytest

from ....channel import Channel, ChannelType

from ..fields import parse_channels


def _iter_options():
    channel_id = 202211050011
    guild_id = 202211050012
    channel_name = 'Faker'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'channels': {},
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'channels': {
                str(channel_id): channel.to_data(defaults = True, include_internals = True),
            },
        },
        guild_id,
        {
            channel_id: channel,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channels(input_data, guild_id):
    """
    Tests whether ``parse_channels`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | dict<int, Channel>`
    """
    return parse_channels(input_data, guild_id)
