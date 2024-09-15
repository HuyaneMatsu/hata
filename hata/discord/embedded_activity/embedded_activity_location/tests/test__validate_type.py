import vampytest

from ..fields import validate_type
from ..preinstanced import EmbeddedActivityLocationType


def _iter_options__passing():
    yield None, EmbeddedActivityLocationType.none
    yield EmbeddedActivityLocationType.guild_channel, EmbeddedActivityLocationType.guild_channel
    yield EmbeddedActivityLocationType.guild_channel.value, EmbeddedActivityLocationType.guild_channel


def _iter_options__type_error():
    yield 12.6


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
    output : ``EmbeddedActivityLocationType``
        
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, EmbeddedActivityLocationType)
    return output
