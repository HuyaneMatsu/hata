import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channels_into


def _iter_options():
    channel_id = 202306080006
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield {}, True, {'channels': []}
    yield {channel_id: channel}, True, {'channels': [channel.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channels_into(input_value, defaults):
    """
    Tests whether ``put_channels_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, Channel>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channels_into(input_value, {}, defaults)
