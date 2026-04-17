import vampytest

from ..preinstanced import VoiceRegion


def _assert_fields_set(voice_region):
    """
    Asserts whether every field are set of the given voice region.
    
    Parameters
    ----------
    voice_region : ``VoiceRegion``
        The instance to test.
    """
    vampytest.assert_instance(voice_region, VoiceRegion)
    vampytest.assert_instance(voice_region.name, str)
    vampytest.assert_instance(voice_region.value, VoiceRegion.VALUE_TYPE)
    vampytest.assert_instance(voice_region.custom, bool)
    vampytest.assert_instance(voice_region.deprecated, bool)
    vampytest.assert_instance(voice_region.vip, bool)


@vampytest.call_from(VoiceRegion.INSTANCES.values())
def test__VoiceRegion__instances(instance):
    """
    Tests whether ``VoiceRegion`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VoiceRegion``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__VoiceRegion__new__min_fields():
    """
    Tests whether ``VoiceRegion.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    # :clueless:
    value = 'vip-eu-zimbabwe'
    
    try:
        output = VoiceRegion(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, 'VIP EU Zimbabwe')
        vampytest.assert_eq(output.custom, True)
        vampytest.assert_eq(output.deprecated, False)
        vampytest.assert_eq(output.vip, True)
        vampytest.assert_is(VoiceRegion.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del VoiceRegion.INSTANCES[value]
        except KeyError:
            pass
