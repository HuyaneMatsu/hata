import vampytest

from ..preinstanced import MessageSearchSortByType


@vampytest.call_from(MessageSearchSortByType.INSTANCES.values())
def test__MessageSearchSortByType__instances(instance):
    """
    Tests whether ``MessageSearchSortByType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageSearchSortByType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageSearchSortByType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageSearchSortByType.VALUE_TYPE)
