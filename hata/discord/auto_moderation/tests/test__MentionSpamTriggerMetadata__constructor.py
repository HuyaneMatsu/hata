import vampytest

from .. import MentionSpamTriggerMetadata


def test__MentionSpamTriggerMetadata__constructor_0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s constructor returns as expected.
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    vampytest.assert_instance(metadata, MentionSpamTriggerMetadata)


def test__MentionSpamTriggerMetadata__constructor_1():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s constructor sets `.mention_limit` as expected.
    Case: `None`.
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    vampytest.assert_instance(metadata.mention_limit, int)


def test__MentionSpamTriggerMetadata__constructor_2():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s constructor sets `.mention_limit` as expected.
    Case: `20`.
    """
    metadata = MentionSpamTriggerMetadata(20)
    
    vampytest.assert_eq(metadata.mention_limit, 20)


def test__MentionSpamTriggerMetadata__constructor_3():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s raises as expected on bad parameter.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        MentionSpamTriggerMetadata(12.6)
