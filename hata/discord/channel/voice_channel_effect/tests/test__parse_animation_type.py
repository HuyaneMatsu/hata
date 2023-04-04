import vampytest

from ..fields import parse_animation_type
from ..preinstanced import VoiceChannelEffectAnimationType


def test__parse_animation_type__0():
    """
    Tests whether `parse_animation_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        ({}, VoiceChannelEffectAnimationType.premium),
        (
            {'animation_type': VoiceChannelEffectAnimationType.basic.value},
            VoiceChannelEffectAnimationType.basic,
        ),
    ):
        output = parse_animation_type(input_value)
        vampytest.assert_is(output, expected_output)
