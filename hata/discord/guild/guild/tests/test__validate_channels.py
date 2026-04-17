import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_channels


def _iter_options__passing():
    channel_id = 202306080007
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield None, {}
    yield [], {}
    yield {}, {}
    yield [channel], {channel_id: channel}
    yield {channel_id: channel}, {channel_id: channel}

    
@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_channels__passing(input_value):
    """
    Tests whether ``validate_channels`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    expected_output : `None | dict<int, Channel>`
    """
    return validate_channels(input_value)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6: 12.6}


@vampytest.raising(TypeError)
@vampytest.call_from(_iter_options__type_error())
def test__validate_channels__type_error(input_value):
    """
    Tests whether ``validate_channels`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_channels(input_value)
