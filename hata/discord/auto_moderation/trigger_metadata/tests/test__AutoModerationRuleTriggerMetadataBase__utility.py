import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase

from .test__AutoModerationRuleTriggerMetadataBase__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataBase__copy():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `copy` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    copy = metadata.copy()
    
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataBase__copy_with():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.copy_with`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    copy = metadata.copy_with()
    
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataBase__placeholders():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s place holders work as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(metadata.excluded_keywords, tuple, nullable = True)
    vampytest.assert_instance(metadata.keyword_presets, tuple, nullable = True)
    vampytest.assert_instance(metadata.keywords, tuple, nullable = True)
    vampytest.assert_instance(metadata.regex_patterns, tuple, nullable = True)
    vampytest.assert_instance(metadata.mention_limit, int)
    vampytest.assert_instance(metadata.raid_protection, bool)


def test__AutoModerationRuleTriggerMetadataBase__iter_excluded_keywords():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.iter_excluded_keywords`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq([*metadata.iter_excluded_keywords()], [])


def test__AutoModerationRuleTriggerMetadataBase__iter_keyword_presets():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.iter_keyword_presets`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq([*metadata.iter_keyword_presets()], [])


def test__AutoModerationRuleTriggerMetadataBase__iter_keywords():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.iter_keywords`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq([*metadata.iter_keywords()], [])


def test__AutoModerationRuleTriggerMetadataBase__iter_regex_patterns():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.iter_regex_patterns`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq([*metadata.iter_regex_patterns()], [])
