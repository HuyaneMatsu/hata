from types import FunctionType

import vampytest

from ..preinstanced import MessageType


def test__MessageType__name():
    """
    Tests whether ``MessageType`` instance names are all strings.
    """
    for instance in MessageType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__MessageType__value():
    """
    Tests whether ``MessageType`` instance values are all the expected value type.
    """
    for instance in MessageType.INSTANCES.values():
        vampytest.assert_instance(instance.value, MessageType.VALUE_TYPE)


def test__MessageType__converter():
    """
    Tests whether ``MessageType`` converters are all the expected value type.
    """
    for instance in MessageType.INSTANCES.values():
        vampytest.assert_instance(instance.converter, FunctionType)


def test__MessageType__deletable():
    """
    Tests whether ``MessageType.deletable``-s are all set as expected.
    """
    for instance in MessageType.INSTANCES.values():
        vampytest.assert_instance(instance.deletable, bool)
