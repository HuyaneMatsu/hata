import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataMentionSpam


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataMentionSpam)


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` sets `.mention_limit` as expected.
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    vampytest.assert_instance(metadata.mention_limit, int)


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` sets `.mention_limit` as expected.
    Case: `20`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(20)
    
    vampytest.assert_eq(metadata.mention_limit, 20)


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataMentionSpam(12.6)
