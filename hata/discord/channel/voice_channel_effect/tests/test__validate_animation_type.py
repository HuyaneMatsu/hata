import vampytest

from ..fields import validate_animation_type
from ..preinstanced import VoiceChannelEffectAnimationType


def test__validate_animation_type():
    """
    Tests whether ``validate_animation_type`` is working as intended.
    """
    for input_value, expected_output in (
        (VoiceChannelEffectAnimationType.basic,  VoiceChannelEffectAnimationType.basic),
        (VoiceChannelEffectAnimationType.basic.value,  VoiceChannelEffectAnimationType.basic),
    ):
        output = validate_animation_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__parse_animation_type__1():
    """
    Tests whether `parse_animation_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_animation_type(input_value)
