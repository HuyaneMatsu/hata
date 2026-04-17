import vampytest

from ..preinstanced import ApplicationTheme


@vampytest.call_from(ApplicationTheme.INSTANCES.values())
def test__ApplicationTheme__instances(instance):
    """
    Tests whether ``ApplicationTheme`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationTheme``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationTheme)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationTheme.VALUE_TYPE)
