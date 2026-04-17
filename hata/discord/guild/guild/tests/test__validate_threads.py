import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_threads


def _iter_options__passing():

    channel_id = 202306130027
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_thread_private,
        name = channel_name,
    )
    
    yield None, None
    yield [], None
    yield {}, None
    yield [channel], {channel_id: channel}
    yield {channel_id: channel}, {channel_id: channel}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_threads(input_value):
    """
    Tests whether ``validate_threads`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<int, Channel>`
    
    Raises
    ------
    TypeError
    """
    output = validate_threads(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
