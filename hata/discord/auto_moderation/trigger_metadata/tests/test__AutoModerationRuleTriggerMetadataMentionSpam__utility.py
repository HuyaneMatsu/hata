import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam

from .test__AutoModerationRuleTriggerMetadataMentionSpam__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.copy`` method works as expected.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy_with__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.copy_with`` method works as expected.
    
    Case: No fields given.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy_with__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.copy_with`` method works as expected.
    
    Case: All fields given.
    """
    old_mention_limit = 20
    new_mention_limit = 19
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(old_mention_limit)
    
    copy = metadata.copy_with(
        mention_limit = new_mention_limit,
    )
    
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(metadata, copy)
    
    vampytest.assert_eq(copy.mention_limit, new_mention_limit)
