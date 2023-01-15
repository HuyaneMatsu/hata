import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam

from .test__AutoModerationRuleTriggerMetadataMentionSpam__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataMentionSpam__copy__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.copy`` method works as expected.
    """
    mention_limit = 20
    raid_protection = True
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(
        mention_limit = mention_limit,
        raid_protection = raid_protection,
    )
    
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
    raid_protection = True
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(
        mention_limit = mention_limit,
        raid_protection = raid_protection,
    )
    
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
    old_raid_protection = True
    new_mention_limit = 19
    new_raid_protection = False
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(
        mention_limit = old_mention_limit,
        raid_protection = old_raid_protection,
    )
    
    copy = metadata.copy_with(
        mention_limit = new_mention_limit,
        raid_protection = new_raid_protection,
    )
    
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(metadata, copy)
    
    vampytest.assert_eq(copy.mention_limit, new_mention_limit)
    vampytest.assert_eq(copy.raid_protection, new_raid_protection)
