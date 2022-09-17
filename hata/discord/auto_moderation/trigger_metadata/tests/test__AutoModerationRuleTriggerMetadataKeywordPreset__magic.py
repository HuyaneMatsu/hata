import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeywordPreset, AutoModerationKeywordPresetType


def test__AutoModerationRuleTriggerMetadataKeywordPreset__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__eq__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataKeywordPreset(None),
        0,
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__eq__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadataKeywordPreset(None, 'owo'),
        AutoModerationRuleTriggerMetadataKeywordPreset(None, 'owo'),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__eq_3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__eq__` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataKeywordPreset(None, 'owo'),
        AutoModerationRuleTriggerMetadataKeywordPreset(None, ['owo', 'awa']),
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__hash__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `__repr__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_instance(repr(metadata), str)
