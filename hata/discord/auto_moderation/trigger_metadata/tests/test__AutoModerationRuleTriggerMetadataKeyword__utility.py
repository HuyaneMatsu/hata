import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeyword


def test__AutoModerationRuleTriggerMetadataKeyword__copy__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.copy`` method works as expected.
    
    Case: no keywords.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeyword__copy__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.copy`` method works as expected.
    
    Case: *n* keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword('owo')
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataKeyword__iter_keywords__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.iter_keywords`` method works as expected.
    
    Case: no keywords.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_eq([*metadata.iter_keywords()], [])


def test__AutoModerationRuleTriggerMetadataKeyword__iter_keywords__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.iter_keywords`` method works as expected.
    
    Case: *n* keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword('owo')
    
    vampytest.assert_eq([*metadata.iter_keywords()], ['owo'])
