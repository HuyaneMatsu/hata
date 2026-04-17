import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_threads


def _iter_options__passing():
    channel_id_0 = 202601080010
    channel_id_1 = 202601080011
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_thread_public,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
    )
    
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
def test__validate_threads(input_value):
    """
    Tests whether ``validate_threads`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to serialise.
    
    Returns
    -------
    output : ``None | tuple<Channel>``
    
    Raises
    ------
    TypeError
    """
    output = validate_threads(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Channel)
    
    return output

