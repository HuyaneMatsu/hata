import vampytest

from ..preinstanced import EntitySelectDefaultValueType


@vampytest.call_from(EntitySelectDefaultValueType.INSTANCES.values())
def test__EntitySelectDefaultValueType__instances(instance):
    """
    Tests whether ``EntitySelectDefaultValueType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EntitySelectDefaultValueType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EntitySelectDefaultValueType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EntitySelectDefaultValueType.VALUE_TYPE)
