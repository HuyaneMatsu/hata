import vampytest

from ..preinstanced import EntitySelectDefaultValueType


def test__EntitySelectDefaultValueType__name():
    """
    Tests whether ``EntitySelectDefaultValueType`` instance names are all strings.
    """
    for instance in EntitySelectDefaultValueType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__EntitySelectDefaultValueType__value():
    """
    Tests whether ``EntitySelectDefaultValueType`` instance values are all the expected value type.
    """
    for instance in EntitySelectDefaultValueType.INSTANCES.values():
        vampytest.assert_instance(instance.value, EntitySelectDefaultValueType.VALUE_TYPE)
