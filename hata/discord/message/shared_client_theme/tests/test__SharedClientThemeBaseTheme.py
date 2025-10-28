import vampytest

from ..preinstanced import SharedClientThemeBaseTheme


@vampytest.call_from(SharedClientThemeBaseTheme.INSTANCES.values())
def test__SharedClientThemeBaseTheme__instances(instance):
    """
    Tests whether ``SharedClientThemeBaseTheme`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SharedClientThemeBaseTheme``
        The instance to test.
    """
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SharedClientThemeBaseTheme.VALUE_TYPE)
