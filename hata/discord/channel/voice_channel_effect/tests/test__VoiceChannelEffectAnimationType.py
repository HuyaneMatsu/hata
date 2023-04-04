import vampytest

from ..preinstanced import VoiceChannelEffectAnimationType


def test__VoiceChannelEffectAnimationType__name():
    """
    Tests whether ``VoiceChannelEffectAnimationType`` instance names are all strings.
    """
    for instance in VoiceChannelEffectAnimationType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__VoiceChannelEffectAnimationType__value():
    """
    Tests whether ``VoiceChannelEffectAnimationType`` instance values are all the expected value type.
    """
    for instance in VoiceChannelEffectAnimationType.INSTANCES.values():
        vampytest.assert_instance(instance.value, VoiceChannelEffectAnimationType.VALUE_TYPE)
