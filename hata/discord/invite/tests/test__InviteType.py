import vampytest

from ..preinstanced import InviteType


def test__InviteType__name():
    """
    Tests whether ``InviteType`` instance names are all strings.
    """
    for instance in InviteType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__InviteType__value():
    """
    Tests whether ``InviteType`` instance values are all the expected value type.
    """
    for instance in InviteType.INSTANCES.values():
        vampytest.assert_instance(instance.value, InviteType.VALUE_TYPE)
