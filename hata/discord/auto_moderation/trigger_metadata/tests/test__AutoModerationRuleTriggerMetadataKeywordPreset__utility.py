import vampytest

from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from ..preinstanced import AutoModerationKeywordPresetType

from .test__AutoModerationRuleTriggerMetadataKeywordPreset__constructor import _assert_fields_set


def test__AutoModerationRuleTriggerMetadataKeywordPreset__copy():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.copy`` works as intended.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(keyword_presets, excluded_keywords)
    
    copy = metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__copy_with__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.copy_with`` works as intended.
    
    Case: No fields.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(keyword_presets, excluded_keywords)
    
    copy = metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
    


def test__AutoModerationRuleTriggerMetadataKeywordPreset__copy_with__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    new_keyword_presets = None
    old_excluded_keywords = ['koishi', 'orin']
    new_excluded_keywords = None
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(old_keyword_presets, old_excluded_keywords)
    
    
    copy = metadata.copy_with(
        keyword_presets = new_keyword_presets,
        excluded_keywords = new_excluded_keywords,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(metadata, copy)
    
    vampytest.assert_eq(copy.keyword_presets, new_keyword_presets)
    vampytest.assert_eq(copy.excluded_keywords, new_excluded_keywords)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_keyword_presets():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.iter_keyword_presets`` works as intended.
    """
    keyword_presents = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    
    for input_keyword_presents, expected_output in (
        (None, []),
        (keyword_presents, keyword_presents),
    ):
        metadata = AutoModerationRuleTriggerMetadataKeywordPreset(keyword_presets = input_keyword_presents)
        vampytest.assert_eq([*metadata.iter_keyword_presets()], expected_output)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__iter_excluded_keywords():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.iter_excluded_keywords`` works as intended.
    """
    keyword_presents = ['koishi', 'orin']
    
    for input_keyword_presents, expected_output in (
        (None, []),
        (keyword_presents, keyword_presents),
    ):
        metadata = AutoModerationRuleTriggerMetadataKeywordPreset(excluded_keywords = input_keyword_presents)
        vampytest.assert_eq([*metadata.iter_excluded_keywords()], expected_output)
