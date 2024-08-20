import vampytest

from ..fields import parse_animation_type
from ..preinstanced import VoiceChannelEffectAnimationType


def _iter_options():
    yield (
        {},
        VoiceChannelEffectAnimationType.premium,
    )
    
    yield (
        {'animation_type': VoiceChannelEffectAnimationType.basic.value},
        VoiceChannelEffectAnimationType.basic,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_animation_type(input_data):
    """
    Tests whether `parse_animation_type` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``VoiceChannelEffectAnimationType``
    """
    output = parse_animation_type(input_data)
    vampytest.assert_instance(output, VoiceChannelEffectAnimationType)
    return output
