import vampytest

from ..preinstanced import SortOrder


@vampytest.call_from(SortOrder.INSTANCES.values())
def test__SortOrder__instances(instance):
    """
    Tests whether ``SortOrder`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SortOrder``
        The instance to test.
    """
    vampytest.assert_instance(instance, SortOrder)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SortOrder.VALUE_TYPE)
