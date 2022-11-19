import vampytest

from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from ..preinstanced import AutoModerationKeywordPresetType


def test__AutoModerationRuleTriggerMetadataKeywordPreset__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__eq__``works as intended.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    keyword_parameters = {
        'keyword_presets': keyword_presets,
        'excluded_keywords': excluded_keywords,
    }
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('keyword_presets', None),
        ('excluded_keywords', None),
    ):
        test_metadata = AutoModerationRuleTriggerMetadataKeywordPreset(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(metadata, test_metadata)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__hash__``works as intended.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(
        keyword_presets,
        excluded_keywords,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__repr__``works as intended.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(
        keyword_presets,
        excluded_keywords,
    )
    
    vampytest.assert_instance(repr(metadata), str)
