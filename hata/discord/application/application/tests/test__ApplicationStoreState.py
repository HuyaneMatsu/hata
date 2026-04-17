import vampytest

from ..preinstanced import ApplicationStoreState


@vampytest.call_from(ApplicationStoreState.INSTANCES.values())
def test__ApplicationStoreState__instances(instance):
    """
    Tests whether ``ApplicationStoreState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationStoreState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationStoreState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationStoreState.VALUE_TYPE)
