import vampytest

from ....channel import ChannelType

from ..fields import validate_channel_type


def _iter_options__passing():
    yield None, ChannelType.guild_text
    yield ChannelType.guild_text, ChannelType.guild_text
    yield ChannelType.guild_text.value, ChannelType.guild_text


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_channel_type__passing(input_value):
    """
    Tests whether ``validate_channel_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ChannelType``
    
    Raises
    ------
    TypeError
    """
    output = validate_channel_type(input_value)
    vampytest.assert_instance(output, ChannelType)
    return output
