import vampytest

from ..preinstanced import VoiceChannelEffectAnimationType


@vampytest.call_from(VoiceChannelEffectAnimationType.INSTANCES.values())
def test__VoiceChannelEffectAnimationType__instances(instance):
    """
    Tests whether ``VoiceChannelEffectAnimationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VoiceChannelEffectAnimationType``
        The instance to test.
    """
    vampytest.assert_instance(instance, VoiceChannelEffectAnimationType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, VoiceChannelEffectAnimationType.VALUE_TYPE)
