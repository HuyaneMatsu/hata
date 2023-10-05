import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channel_into


def _iter_options():
    channel_id = 202212230002
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, name = 'Hotaru')
    
    yield (channel, False, {'channel': channel.to_data(defaults = False, include_internals = True)})
    yield (channel, True, {'channel': channel.to_data(defaults = True, include_internals = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel_into(input_value, defaults):
    """
    Tests whether ``put_channel_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``Channel``
        Value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channel_into(input_value, {}, defaults)
