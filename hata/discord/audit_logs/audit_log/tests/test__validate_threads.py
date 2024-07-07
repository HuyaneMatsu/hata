import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_threads


def _iter_options__passing():
    channel_id_0 = 202406270012
    channel_id_1 = 202406270013
    guild_id = 202406270014
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    channel_1 = Channel.precreate(channel_id_1, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)

    yield None, None
    yield [], None
    yield [channel_0], {channel_id_0: channel_0}
    yield (
        [channel_0, channel_0],
        {channel_id_0: channel_0},
    )
    yield (
        [channel_1, channel_0],
        {channel_id_0: channel_0, channel_id_1: channel_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_threads(input_value):
    """
    Validates whether ``validate_threads`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, ClientChannelBase>`
    
    Raises
    ------
    TypeError
    """
    output = validate_threads(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
