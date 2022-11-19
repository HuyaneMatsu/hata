import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam

from .test__AutoModerationRuleTriggerMetadataMentionSpam__constructor import _assert_is_every_attribute_set


def test__AutoModerationRuleTriggerMetadataMentionSpam__to_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.to_data`` works as expected.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        {
            'mention_total_limit': mention_limit
        }
    )



def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.from_data`` works as expected.
    """
    mention_limit = 20
    
    data = {
        'mention_total_limit': mention_limit
    }
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data(data)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.mention_limit, mention_limit)
