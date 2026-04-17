import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channels_and_channel_datas


def _iter_options():
    channel_id = 202306290002
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield None, True, {'channels': []}
    yield None, False, {'channels': []}
    yield [channel], True, {'channels': [channel.to_data(defaults = True, include_internals = True)]}
    yield [channel], False, {'channels': [channel.to_data(defaults = False, include_internals = True)]}
    yield [{'name': channel_name}], True, {'channels': [{'name': channel_name}]}
    yield (
        [channel, {'name': channel_name}],
        True,
        {'channels': [channel.to_data(defaults = True, include_internals = True), {'name': channel_name}]},
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channels_and_channel_datas(input_value, defaults):
    """
    Tests whether ``put_channels_and_channel_datas`` works as intended.
    
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
    return put_channels_and_channel_datas(input_value, {}, defaults)
