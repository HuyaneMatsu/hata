import vampytest

from ..preinstanced import Theme


@vampytest.call_from(Theme.INSTANCES.values())
def test__Theme__instances(instance):
    """
    Tests whether ``Theme`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Theme``
        The instance to test.
    """
    vampytest.assert_instance(instance, Theme)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, Theme.VALUE_TYPE)
