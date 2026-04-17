import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import put_channels


def _iter_options():
    channel_id_0 = 202305190005
    channel_name_0 = 'Far'
    
    channel_id_1 = 202305190006
    channel_name_1 = 'East'
    
    channel_0 = GuildWidgetChannel(
        channel_id = channel_id_0,
        name = channel_name_0,
    )
    
    channel_1 = GuildWidgetChannel(
        channel_id = channel_id_1,
        name = channel_name_1,
    )
    
    yield (
        None,
        False,
        {
            'channels': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'channels': [],
        },
    )
    
    yield (
        (
            channel_0, 
            channel_1,
        ),
        False,
        {
            'channels': [
                channel_0.to_data(defaults = False),
                channel_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        (
            channel_0,
            channel_1,
        ),
        True,
        {
            'channels': [
                channel_0.to_data(defaults = True),
                channel_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channels(input_value, defaults):
    """
    Tests whether ``put_channels`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<GuildWidgetChannel>``
        Input value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channels(input_value, {}, defaults)
