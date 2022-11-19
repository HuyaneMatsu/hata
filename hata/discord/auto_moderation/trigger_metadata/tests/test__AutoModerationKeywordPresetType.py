import vampytest

from ..preinstanced import AutoModerationKeywordPresetType


def test__AutoModerationKeywordPresetType__name():
    """
    Tests whether ``AutoModerationKeywordPresetType`` instance names are all strings.
    """
    for instance in AutoModerationKeywordPresetType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationKeywordPresetType__value():
    """
    Tests whether ``AutoModerationKeywordPresetType`` instance values are all the expected value type.
    """
    for instance in AutoModerationKeywordPresetType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationKeywordPresetType.VALUE_TYPE)
