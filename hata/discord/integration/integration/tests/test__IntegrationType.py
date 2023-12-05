import vampytest

from ..preinstanced import IntegrationType


@vampytest.call_from(IntegrationType.INSTANCES.values())
def test__IntegrationType__instances(instance):
    """
    Tests whether ``IntegrationType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``IntegrationType``
        The instance to test.
    """
    vampytest.assert_instance(instance, IntegrationType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, IntegrationType.VALUE_TYPE)
