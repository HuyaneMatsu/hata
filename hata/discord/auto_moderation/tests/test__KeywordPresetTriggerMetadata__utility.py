import vampytest

from .. import KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType


def test__KeywordPresetTriggerMetadata__copy_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `copy` method works as expected.
    Case: no keywords presets.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordPresetTriggerMetadata__copy_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `copy` method works as expected.
    Case: *n* keyword preset(s).
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordPresetTriggerMetadata__iter_keywords_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_keywords` method works as expected.
    Case: no keywords presets.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [])


def test__KeywordPresetTriggerMetadata__iter_keywords_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_keywords` method works as expected.
    Case: *n* keyword preset(s).
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [AutoModerationKeywordPresetType.slur])
