import vampytest

from ...guild_widget_channel import GuildWidgetChannel

from ..fields import validate_channels


def _iter_options__passing():
    channel_id_0 = 202305190007
    channel_id_1 = 202305190008
    
    channel_0 = GuildWidgetChannel(channel_id = channel_id_0)
    channel_1 = GuildWidgetChannel(channel_id = channel_id_1)
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            channel_0,
            channel_1,
        ],
        (
            channel_0,
            channel_1,
        ),
    )
    
    yield (
        [
            channel_1,
            channel_0,
        ],
        (
            channel_0,
            channel_1,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_channels(input_value):
    """
    Validates whether ``validate_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        value to validate.
    
    Returns
    -------
    output : ``None | dict<GuildWidgetChannel>``
    
    Raises
    ------
    TypeError
    """
    output = validate_channels(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildWidgetChannel)
    
    return output
