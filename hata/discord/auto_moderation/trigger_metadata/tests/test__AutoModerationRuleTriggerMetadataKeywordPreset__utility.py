import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeywordPreset, AutoModerationKeywordPresetType


def test__AutoModerationRuleTriggerMetadataKeywordPreset__copy__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `copy` method works as expected.
    Case: no keywords presets.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__copy__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `copy` method works as expected.
    Case: *n* keyword preset(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur, 'owo')
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_keyword_presets_0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `iter_keyword_presets` method works as expected.
    Case: no keywords presets.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [])


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_keyword_presets__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `iter_keyword_presets` method works as expected.
    Case: *n* keyword preset(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [AutoModerationKeywordPresetType.slur])


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_excluded_keywords__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `iter_excluded_keywords` method works as expected.
    Case: no excluded keywords.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None)
    
    vampytest.assert_eq([*metadata.iter_excluded_keywords()], [])


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_excluded_keywords__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset``'s `iter_excluded_keywords` method works as expected.
    Case: *n* excluded keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(None, 'owo')
    
    vampytest.assert_eq([*metadata.iter_excluded_keywords()], ['owo'])
