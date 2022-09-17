import vampytest

from .. import AutoModerationActionType, AutoModerationActionMetadataBase


def test__AutoModerationActionType__name():
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationActionType__value():
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationActionType.VALUE_TYPE)


def test__AutoModerationActionType__metadata_type():
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, AutoModerationActionMetadataBase, nullable=True)
