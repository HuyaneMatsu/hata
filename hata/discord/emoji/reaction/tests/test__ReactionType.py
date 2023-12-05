import vampytest

from ..preinstanced import ReactionType


@vampytest.call_from(ReactionType.INSTANCES.values())
def test__ReactionType__instances(instance):
    """
    Tests whether ``ReactionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ReactionType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ReactionType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ReactionType.VALUE_TYPE)
