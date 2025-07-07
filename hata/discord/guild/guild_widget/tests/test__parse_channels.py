import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import parse_channels


def _iter_options():
    channel_id_0 = 202305190003
    channel_name_0 = 'Far'
    
    channel_id_1 = 202305190004
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
        {},
        None,
    )
    
    yield (
        {
            'channels': None,
        },
        None,
    )
    
    yield (
        {
            'channels': [],
        },
        None,
    )
    
    yield (
        {
            'channels': [
                channel_0.to_data(),
                channel_1.to_data(),
            ],
        },
        (
            channel_0,
            channel_1,
        ),
    )
    
    yield (
        {
            'channels': [
                channel_1.to_data(),
                channel_0.to_data(),
            ],
        },
        (
            channel_0,
            channel_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channels(input_data):
    """
    Tests whether ``parse_channels`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<GuildWidgetChannel>``
    """
    output = parse_channels(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildWidgetChannel)
    
    return output
