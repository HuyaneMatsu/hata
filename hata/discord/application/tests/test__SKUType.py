import vampytest

from .. import EntitlementType


def test__EntitlementType__name():
    """
    Tests whether ``EntitlementType`` instance names are all strings.
    """
    for instance in EntitlementType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__EntitlementType__value():
    """
    Tests whether ``EntitlementType`` instance values are all the expected value type.
    """
    for instance in EntitlementType.INSTANCES.values():
        vampytest.assert_instance(instance.value, EntitlementType.VALUE_TYPE)
