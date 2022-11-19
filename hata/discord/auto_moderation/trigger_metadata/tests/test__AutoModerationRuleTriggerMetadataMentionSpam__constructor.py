import vampytest

from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether all attributes are set of the given rule trigger metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationRuleTriggerMetadataMentionSpam``
        The metadata object to check.
    """
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataMentionSpam)
    vampytest.assert_instance(metadata.mention_limit, int)


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` work as intended.
    
    Case: No parameters given.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam()
    _assert_is_every_attribute_set(metadata)


def test__AutoModerationRuleTriggerMetadataMentionSpam__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam.__new__`` work as intended.
    
    Case: stuffed.
    """
    mention_limit = 20
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.mention_limit, mention_limit)
