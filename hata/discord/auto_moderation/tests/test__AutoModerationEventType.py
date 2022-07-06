import vampytest

from .. import AutoModerationEventType


def test__AutoModerationEventType__name():
    for instance in AutoModerationEventType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationEventType__value():
    for instance in AutoModerationEventType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationEventType.VALUE_TYPE)
