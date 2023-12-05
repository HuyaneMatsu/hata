import vampytest

from ..preinstanced import ApplicationMonetizationState


@vampytest.call_from(ApplicationMonetizationState.INSTANCES.values())
def test__ApplicationMonetizationState__instances(instance):
    """
    Tests whether ``ApplicationMonetizationState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationMonetizationState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationMonetizationState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationMonetizationState.VALUE_TYPE)
    vampytest.assert_instance(instance.enabled, bool)
    vampytest.assert_instance(instance.locked, bool)
    vampytest.assert_instance(instance.settable, bool)
