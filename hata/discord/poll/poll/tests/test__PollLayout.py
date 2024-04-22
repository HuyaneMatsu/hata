import vampytest

from ..preinstanced import PollLayout


@vampytest.call_from(PollLayout.INSTANCES.values())
def test__PollLayout__instances(instance):
    """
    Tests whether ``PollLayout`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``PollLayout``
        The instance to test.
    """
    vampytest.assert_instance(instance, PollLayout)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, PollLayout.VALUE_TYPE)
