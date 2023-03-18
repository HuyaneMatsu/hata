import vampytest

from ..preinstanced import ScheduledEventStatus


def test__ScheduledEventStatus__name():
    """
    Tests whether ``ScheduledEventStatus`` instance names are all strings.
    """
    for instance in ScheduledEventStatus.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ScheduledEventStatus__value():
    """
    Tests whether ``ScheduledEventStatus`` instance values are all the expected value type.
    """
    for instance in ScheduledEventStatus.INSTANCES.values():
        vampytest.assert_instance(instance.value, ScheduledEventStatus.VALUE_TYPE)
