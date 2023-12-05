import vampytest

from ..preinstanced import EntitlementType


@vampytest.call_from(EntitlementType.INSTANCES.values())
def test__EntitlementType__instances(instance):
    """
    Tests whether ``EntitlementType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EntitlementType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EntitlementType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EntitlementType.VALUE_TYPE)
