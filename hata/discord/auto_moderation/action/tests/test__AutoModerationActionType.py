import vampytest

from ...action_metadata import AutoModerationActionMetadataBase

from ..preinstanced import AutoModerationActionType


def test__AutoModerationActionType__name():
    """
    Tests whether ``AutoModerationActionMetadataBase.name`` are all correctly set.
    """
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationActionType__value():
    """
    Tests whether ``AutoModerationActionMetadataBase.value`` are all correctly set.
    """
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationActionType.VALUE_TYPE)


def test__AutoModerationActionType__metadata_type():
    """
    Tests whether ``AutoModerationActionMetadataBase.metadata_type`` are all correctly set.
    """
    for instance in AutoModerationActionType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, AutoModerationActionMetadataBase)
