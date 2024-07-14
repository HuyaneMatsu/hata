import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_threads_into


def _iter_options():
    channel_id = 202306130026
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_thread_private,
        name = channel_name,
    )
    
    yield None, False, {'threads': []}
    yield None, True, {'threads': []}
    yield {channel_id: channel}, False, {'threads': [channel.to_data(defaults = False, include_internals = True)]}
    yield {channel_id: channel}, True, {'threads': [channel.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_threads_into(input_value, defaults):
    """
    Tests whether ``put_threads_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, Channel>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_threads_into(input_value, {}, defaults)
