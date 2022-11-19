import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam


def test__AutoModerationRuleTriggerMetadataMentionSpam__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__eq__`` works as intended.
    """
    mention_limit = 20
    
    keyword_parameters = {
        'mention_limit': mention_limit
    }
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('mention_limit', 19),
    ):
        test_metadata = AutoModerationRuleTriggerMetadataMentionSpam(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
        


def test__AutoModerationRuleTriggerMetadataMentionSpam__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__hash__`` works as intended.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataMentionSpam__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__repr__`` works as intended.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    
    vampytest.assert_instance(repr(metadata), str)
