import vampytest

from ..preinstanced import AutoModerationEventType


def test__AutoModerationEventType__name():
    """
    Tests whether ``AutoModerationEventType`` instances have their `.name` set correctly.
    """
    for instance in AutoModerationEventType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationEventType__value():
    """
    Tests whether ``AutoModerationEventType`` instances have their `.value` set correctly.
    """
    for instance in AutoModerationEventType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationEventType.VALUE_TYPE)
