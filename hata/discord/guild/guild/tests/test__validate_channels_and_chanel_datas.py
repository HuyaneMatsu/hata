import vampytest

from ....channel import Channel, ChannelType

from ..fields import validate_channels_and_channel_datas


def iter_options__passing():
    channel_id = 20230606290000
    channel_name = 'Koishi'
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        name = channel_name,
    )
    
    yield None, None
    yield [], None
    yield [channel], [channel]
    yield [{'name': channel_name}], [{'name': channel_name}]
    yield [channel, {'name': channel_name}], [channel, {'name': channel_name}]

    
@vampytest._(vampytest.call_from(iter_options__passing()).returning_last())
def test__validate_channels_and_channel_datas__passing(input_value):
    """
    Tests whether ``validate_channels_and_channel_datas`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    expected_output : `None | list<Channel | dict>`
    """
    return validate_channels_and_channel_datas(input_value)


def iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {}


@vampytest.raising(TypeError)
@vampytest.call_from(iter_options__type_error())
def test__validate_channels_and_channel_datas__type_error(input_value):
    """
    Tests whether ``validate_channels_and_channel_datas`` works as intended.
    
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
    validate_channels_and_channel_datas(input_value)
