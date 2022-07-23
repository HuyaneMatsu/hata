import vampytest

from .. import MentionSpamTriggerMetadata


def test__MentionSpamTriggerMetadata__eq_0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        MentionSpamTriggerMetadata(None),
        MentionSpamTriggerMetadata(None),
    )


def test__MentionSpamTriggerMetadata__eq_1():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        MentionSpamTriggerMetadata(None),
        0,
    )


def test__MentionSpamTriggerMetadata__not_eq_0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `__eq__` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        MentionSpamTriggerMetadata(None),
        MentionSpamTriggerMetadata(20),
    )


def test__MentionSpamTriggerMetadata__hash():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `__hash__` method works as intended
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__MentionSpamTriggerMetadata__repr():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `__repr__` method works as intended
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    vampytest.assert_instance(repr(metadata), str)
