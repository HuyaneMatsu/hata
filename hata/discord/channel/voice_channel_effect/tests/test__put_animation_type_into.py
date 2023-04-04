import vampytest

from ..fields import put_animation_type_into
from ..preinstanced import VoiceChannelEffectAnimationType


def test__put_animation_type_into():
    """
    Tests whether ``put_animation_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (
            VoiceChannelEffectAnimationType.basic,
            True,
            {'animation_type': VoiceChannelEffectAnimationType.basic.value},
        ),
    ):
        data = put_animation_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
