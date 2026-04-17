import vampytest

from ..preinstanced import HubType


@vampytest.call_from(HubType.INSTANCES.values())
def test__HubType__instances(instance):
    """
    Tests whether ``HubType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``HubType``
        The instance to test.
    """
    vampytest.assert_instance(instance, HubType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, HubType.VALUE_TYPE)
