import vampytest

from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from ..preinstanced import AutoModerationKeywordPresetType


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether all attributes are set of the given rule trigger metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationRuleTriggerMetadataKeywordPreset``
        The metadata object to check.
    """
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataKeywordPreset)
    vampytest.assert_instance(metadata.excluded_keywords, tuple, nullable = True)
    vampytest.assert_instance(metadata.keyword_presets, tuple, nullable = True)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` returns as expected.
    
    Case: No parameters.
    """
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset()
    _assert_is_every_attribute_set(metadata)


def test__AutoModerationRuleTriggerMetadataKeywordPreset__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeywordPreset.__new__`` returns as expected.
    
    Case: All parameters.
    """
    keyword_presets = [AutoModerationKeywordPresetType.cursing, AutoModerationKeywordPresetType.slur]
    excluded_keywords = ['koishi', 'orin']
    
    metadata = AutoModerationRuleTriggerMetadataKeywordPreset(
        keyword_presets,
        excluded_keywords,
    )
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.keyword_presets, tuple(keyword_presets))
    vampytest.assert_eq(metadata.excluded_keywords, tuple(excluded_keywords))
