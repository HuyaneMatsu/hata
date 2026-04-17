import vampytest

from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from ..preinstanced import AutoModerationKeywordPresetType

from .test__AutoModerationRuleTriggerMetadataKeywordPreset__constructor import _assert_fields_set


def test__AutoModerationRuleTriggerMetadataKeywordPreset__to_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.to_data`` works as intended.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(keyword_presets, excluded_keywords)
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),{
            'presets': [keyword_preset.value for keyword_preset in keyword_presets],
            'allow_list': excluded_keywords,
        },
    )


def test__AutoModerationRuleTriggerMetadataKeywordPreset__from_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.from_data`` works as intended.
    None value cases.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    data = {
        'presets': [keyword_preset.value for keyword_preset in keyword_presets],
        'allow_list': excluded_keywords,
    }
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset.from_data(data)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.keyword_presets, tuple(keyword_presets))
    vampytest.assert_eq(metadata.excluded_keywords, tuple(excluded_keywords))
