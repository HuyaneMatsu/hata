import vampytest

from ..preinstanced import ApplicationDiscoverabilityState


@vampytest.call_from(ApplicationDiscoverabilityState.INSTANCES.values())
def test__ApplicationDiscoverabilityState__instances(instance):
    """
    Tests whether ``ApplicationDiscoverabilityState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationDiscoverabilityState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationDiscoverabilityState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationDiscoverabilityState.VALUE_TYPE)
