import vampytest

from .. import AutoModerationKeywordPresetType


def test__AutoModerationKeywordPresetType__name():
    for instance in AutoModerationKeywordPresetType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationKeywordPresetType__value():
    for instance in AutoModerationKeywordPresetType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationKeywordPresetType.VALUE_TYPE)
