import vampytest

from ..preinstanced import ConnectionVisibility


@vampytest.call_from(ConnectionVisibility.INSTANCES.values())
def test__ConnectionVisibility__instances(instance):
    """
    Tests whether ``ConnectionVisibility`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ConnectionVisibility``
        The instance to test.
    """
    vampytest.assert_instance(instance, ConnectionVisibility)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ConnectionVisibility.VALUE_TYPE)
