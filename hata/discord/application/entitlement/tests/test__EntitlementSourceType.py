import vampytest

from ..preinstanced import EntitlementSourceType


@vampytest.call_from(EntitlementSourceType.INSTANCES.values())
def test__EntitlementSourceType__instances(instance):
    """
    Tests whether ``EntitlementSourceType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EntitlementSourceType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EntitlementSourceType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EntitlementSourceType.VALUE_TYPE)
