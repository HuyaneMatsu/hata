import vampytest

from ..preinstanced import IntegrationExpireBehavior


@vampytest.call_from(IntegrationExpireBehavior.INSTANCES.values())
def test__IntegrationExpireBehavior__instances(instance):
    """
    Tests whether ``IntegrationExpireBehavior`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``IntegrationExpireBehavior``
        The instance to test.
    """
    vampytest.assert_instance(instance, IntegrationExpireBehavior)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, IntegrationExpireBehavior.VALUE_TYPE)
