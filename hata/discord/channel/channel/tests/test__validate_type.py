import vampytest

from ..fields import validate_type
from ..preinstanced import ChannelType


def _iter_options__passing():
    yield None, ChannelType.guild_text
    yield ChannelType.guild_text, ChannelType.guild_text
    yield ChannelType.guild_text.value, ChannelType.guild_text


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
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
    output = validate_type(input_value)
    vampytest.assert_instance(output, ChannelType)
    return output
