import vampytest

from ..preinstanced import ApplicationIntegrationType


@vampytest.call_from(ApplicationIntegrationType.INSTANCES.values())
def test__ApplicationIntegrationType__instances(instance):
    """
    Tests whether ``ApplicationIntegrationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationIntegrationType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationIntegrationType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationIntegrationType.VALUE_TYPE)
