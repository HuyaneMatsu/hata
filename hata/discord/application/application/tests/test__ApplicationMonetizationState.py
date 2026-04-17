import vampytest

from ..preinstanced import ApplicationMonetizationState


def _assert_fields_set(application_monetization_state):
    """
    Asserts whether every field are set of the given application monetization state.
    
    Parameters
    ----------
    application_monetization_state : ``ApplicationMonetizationState``
        The instance to test.
    """
    vampytest.assert_instance(application_monetization_state, ApplicationMonetizationState)
    vampytest.assert_instance(application_monetization_state.name, str)
    vampytest.assert_instance(application_monetization_state.value, ApplicationMonetizationState.VALUE_TYPE)
    vampytest.assert_instance(application_monetization_state.enabled, bool)
    vampytest.assert_instance(application_monetization_state.locked, bool)
    vampytest.assert_instance(application_monetization_state.settable, bool)


@vampytest.call_from(ApplicationMonetizationState.INSTANCES.values())
def test__ApplicationMonetizationState__instances(instance):
    """
    Tests whether ``ApplicationMonetizationState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationMonetizationState``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ApplicationMonetizationState__new__min_fields():
    """
    Tests whether ``ApplicationMonetizationState.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ApplicationMonetizationState(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ApplicationMonetizationState.NAME_DEFAULT)
        vampytest.assert_eq(output.enabled, False)
        vampytest.assert_eq(output.locked, False)
        vampytest.assert_eq(output.settable, False)
        vampytest.assert_is(ApplicationMonetizationState.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ApplicationMonetizationState.INSTANCES[value]
        except KeyError:
            pass
