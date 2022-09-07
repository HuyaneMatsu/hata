import vampytest

from .. import MentionSpamTriggerMetadata


def test__MentionSpamTriggerMetadata__copy__0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `copy` method works as expected.
    Case: no mention limit.
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__MentionSpamTriggerMetadata__copy__1():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `copy` method works as expected.
    Case: `20`.
    """
    metadata = MentionSpamTriggerMetadata(20)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
