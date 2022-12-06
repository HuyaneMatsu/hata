from types import FunctionType

import vampytest

from ..preinstanced import ApplicationRoleConnectionValueType


def test__ApplicationRoleConnectionValueType__name():
    """
    Tests whether ``ApplicationRoleConnectionValueType`` instance names are all strings.
    """
    for instance in ApplicationRoleConnectionValueType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationRoleConnectionValueType__value():
    """
    Tests whether ``ApplicationRoleConnectionValueType`` instance values are all the expected value type.
    """
    for instance in ApplicationRoleConnectionValueType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationRoleConnectionValueType.VALUE_TYPE)


def test__ApplicationRoleConnectionValueType__serializer():
    """
    Tests whether ``ApplicationRoleConnectionValueType.serializer``-s are all set correctly.
    """
    for instance in ApplicationRoleConnectionValueType.INSTANCES.values():
        vampytest.assert_instance(instance.serializer, FunctionType)


def test__ApplicationRoleConnectionValueType__deserializer():
    """
    Tests whether ``ApplicationRoleConnectionValueType.deserializer``-s are all set correctly.
    """
    for instance in ApplicationRoleConnectionValueType.INSTANCES.values():
        vampytest.assert_instance(instance.deserializer, FunctionType)
