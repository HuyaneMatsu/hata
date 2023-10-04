import vampytest

from ..preinstanced import EntitlementOwnerType


def test__EntitlementOwnerType__name():
    """
    Tests whether ``EntitlementOwnerType`` instance names are all strings.
    """
    for instance in EntitlementOwnerType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__EntitlementOwnerType__value():
    """
    Tests whether ``EntitlementOwnerType`` instance values are all the expected value type.
    """
    for instance in EntitlementOwnerType.INSTANCES.values():
        vampytest.assert_instance(instance.value, EntitlementOwnerType.VALUE_TYPE)
