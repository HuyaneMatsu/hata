import vampytest

from ..fields import put_animation_type_into
from ..preinstanced import VoiceChannelEffectAnimationType


def _iter_options():
    yield (
        VoiceChannelEffectAnimationType.premium,
        False,
        {},
    )
    
    yield (
        VoiceChannelEffectAnimationType.premium,
        True,
        {'animation_type': VoiceChannelEffectAnimationType.premium.value},
    )
    
    yield (
        VoiceChannelEffectAnimationType.basic,
        False,
        {'animation_type': VoiceChannelEffectAnimationType.basic.value},
    )
    
    yield (
        VoiceChannelEffectAnimationType.basic,
        True,
        {'animation_type': VoiceChannelEffectAnimationType.basic.value},
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_animation_type_into(input_value, defaults):
    """
    Tests whether ``put_animation_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``VoiceChannelEffectAnimationType``
        The value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_animation_type_into(input_value, {}, defaults)
