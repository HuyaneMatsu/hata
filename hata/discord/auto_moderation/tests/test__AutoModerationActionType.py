import vampytest

from .. import AutoModerationActionType


def test__AutoModerationActionType__name():
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationActionType__value():
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationActionType.VALUE_TYPE)
