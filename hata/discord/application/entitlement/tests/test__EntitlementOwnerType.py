import vampytest

from ..preinstanced import EntitlementOwnerType


@vampytest.call_from(EntitlementOwnerType.INSTANCES.values())
def test__EntitlementOwnerType__instances(instance):
    """
    Tests whether ``EntitlementOwnerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EntitlementOwnerType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EntitlementOwnerType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EntitlementOwnerType.VALUE_TYPE)
