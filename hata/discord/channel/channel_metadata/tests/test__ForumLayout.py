import vampytest

from ..preinstanced import ForumLayout


@vampytest.call_from(ForumLayout.INSTANCES.values())
def test__ForumLayout__instances(instance):
    """
    Tests whether ``ForumLayout`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ForumLayout``
        The instance to test.
    """
    vampytest.assert_instance(instance, ForumLayout)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ForumLayout.VALUE_TYPE)
