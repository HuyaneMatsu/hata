import vampytest

from ..preinstanced import HubType


def test__HubType__name():
    """
    Tests whether ``HubType`` instance names are all strings.
    """
    for instance in HubType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__HubType__value():
    """
    Tests whether ``HubType`` instance values are all the expected value type.
    """
    for instance in HubType.INSTANCES.values():
        vampytest.assert_instance(instance.value, HubType.VALUE_TYPE)
