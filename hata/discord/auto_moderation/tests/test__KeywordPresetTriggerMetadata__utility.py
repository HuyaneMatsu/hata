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
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur, 'owo')
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__KeywordPresetTriggerMetadata__iter_keyword_presets_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_keyword_presets` method works as expected.
    Case: no keywords presets.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [])


def test__KeywordPresetTriggerMetadata__iter_keyword_presets_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_keyword_presets` method works as expected.
    Case: *n* keyword preset(s).
    """
    metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.slur)
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [AutoModerationKeywordPresetType.slur])


def test__KeywordPresetTriggerMetadata__iter_excluded_keywords_0():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_excluded_keywords` method works as expected.
    Case: no excluded keywords.
    """
    metadata = KeywordPresetTriggerMetadata(None)
    
    vampytest.assert_eq([*metadata.iter_excluded_keywords()], [])


def test__KeywordPresetTriggerMetadata__iter_excluded_keywords_1():
    """
    Tests whether ``KeywordPresetTriggerMetadata``'s `iter_excluded_keywords` method works as expected.
    Case: *n* excluded keyword(s).
    """
    metadata = KeywordPresetTriggerMetadata(None, 'owo')
    
    vampytest.assert_eq([*metadata.iter_excluded_keywords()], ['owo'])
