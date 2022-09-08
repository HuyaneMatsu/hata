import vampytest

from .. import ActivityType


def test__ActivityType__name():
    """
    Tests whether ``ActivityType`` instance names are all strings.
    """
    for instance in ActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ActivityType__value():
    """
    Tests whether ``ActivityType`` instance values are all the expected value type.
    """
    for instance in ActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ActivityType.VALUE_TYPE)
