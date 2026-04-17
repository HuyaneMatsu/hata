import vampytest

from ..fields import validate_animation_type
from ..preinstanced import VoiceChannelEffectAnimationType


def _iter_options__passing():
    yield None, VoiceChannelEffectAnimationType.premium
    yield VoiceChannelEffectAnimationType.basic,  VoiceChannelEffectAnimationType.basic
    yield VoiceChannelEffectAnimationType.basic.value,  VoiceChannelEffectAnimationType.basic


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_animation_type(input_value):
    """
    Tests whether ``validate_animation_type`` is working as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    output = validate_animation_type(input_value)
    vampytest.assert_instance(output, VoiceChannelEffectAnimationType)
    return output
