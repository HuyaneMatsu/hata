import vampytest

from ..preinstanced import MessageSearchSortOrderType


@vampytest.call_from(MessageSearchSortOrderType.INSTANCES.values())
def test__MessageSearchSortOrderType__instances(instance):
    """
    Tests whether ``MessageSearchSortOrderType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageSearchSortOrderType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageSearchSortOrderType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageSearchSortOrderType.VALUE_TYPE)
