import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataMentionSpam


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `copy` method works as expected.
    Case: no mention limit.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `copy` method works as expected.
    Case: `20`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(20)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
