import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_threads


def _iter_options():
    channel_id_0 = 202406250012
    channel_id_1 = 202406250013
    guild_id = 202406250014
    
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'threads': [],
        },
    )
    
    yield (
        {
            channel_id_0: channel_0,
            channel_id_1: channel_1,
        },
        False,
        {
            'threads': [
                channel_0.to_data(defaults = False, include_internals = True),
                channel_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            channel_id_0: channel_0,
            channel_id_1: channel_1,
        },
        True,
        {
            'threads': [
                channel_0.to_data(defaults = True, include_internals = True),
                channel_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_threads(input_value, defaults):
    """
    Tests whether ``put_threads`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, Channel>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_threads(input_value, {}, defaults)
