import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam

from .test__AutoModerationRuleTriggerMetadataMentionSpam__constructor import _assert_fields_set


def test__AutoModerationRuleTriggerMetadataMentionSpam__to_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.to_data`` works as expected.
    """
    mention_limit = 20
    raid_protection = True
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(
        mention_limit = mention_limit,
        raid_protection = raid_protection,
    )
    
    expected_output = {
        'mention_total_limit': mention_limit,
        'mention_raid_protection_enabled': raid_protection,
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_output,
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.from_data`` works as expected.
    """
    mention_limit = 20
    raid_protection = True
    
    data = {
        'mention_total_limit': mention_limit,
        'mention_raid_protection_enabled': raid_protection,
    }
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data(data)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.mention_limit, mention_limit)
    vampytest.assert_eq(metadata.raid_protection, raid_protection)
