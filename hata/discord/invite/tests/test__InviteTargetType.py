import vampytest

from ..preinstanced import InviteTargetType


def test__InviteTargetType__name():
    """
    Tests whether ``InviteTargetType`` instance names are all strings.
    """
    for instance in InviteTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__InviteTargetType__value():
    """
    Tests whether ``InviteTargetType`` instance values are all the expected value type.
    """
    for instance in InviteTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.value, InviteTargetType.VALUE_TYPE)
