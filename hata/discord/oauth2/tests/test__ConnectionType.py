import vampytest

from .. import ConnectionType


def test__ConnectionType__name():
    """
    Tests whether ``ConnectionType`` instance names are all strings.
    """
    for instance in ConnectionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ConnectionType__value():
    """
    Tests whether ``ConnectionType`` instance values are all the expected value type.
    """
    for instance in ConnectionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ConnectionType.VALUE_TYPE)
