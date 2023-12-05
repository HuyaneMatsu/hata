import vampytest

from ..preinstanced import ConnectionType


@vampytest.call_from(ConnectionType.INSTANCES.values())
def test__ConnectionType__instances(instance):
    """
    Tests whether ``ConnectionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ConnectionType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ConnectionType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ConnectionType.VALUE_TYPE)
