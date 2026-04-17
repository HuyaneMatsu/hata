import vampytest

from ..preinstanced import SubscriptionStatus


@vampytest.call_from(SubscriptionStatus.INSTANCES.values())
def test__SubscriptionStatus__instances(instance):
    """
    Tests whether ``SubscriptionStatus`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SubscriptionStatus``
        The instance to test.
    """
    vampytest.assert_instance(instance, SubscriptionStatus)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SubscriptionStatus.VALUE_TYPE)
