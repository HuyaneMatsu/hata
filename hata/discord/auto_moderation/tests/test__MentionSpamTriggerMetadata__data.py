import vampytest

from .. import MentionSpamTriggerMetadata


def test__MentionSpamTriggerMetadata__to_data__0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = MentionSpamTriggerMetadata(None)
    
    vampytest.assert_instance(metadata.to_data()['mention_total_limit'], int)


def test__MentionSpamTriggerMetadata__to_data__1():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = MentionSpamTriggerMetadata(20)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'mention_total_limit': 20,
        },
    )


def test__MentionSpamTriggerMetadata__from_data__0():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = MentionSpamTriggerMetadata.from_data({
        'mention_total_limit': None,
    })
    
    vampytest.assert_eq(
        metadata,
        MentionSpamTriggerMetadata(None),
    )


def test__MentionSpamTriggerMetadata__from_data__1():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `from_data` method works as expected.
    Case: *missing*.
    """
    metadata = MentionSpamTriggerMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        MentionSpamTriggerMetadata(None),
    )


def test__MentionSpamTriggerMetadata__from_data__2():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = MentionSpamTriggerMetadata.from_data({
        'mention_total_limit': None,
    })
    
    vampytest.assert_eq(
        metadata,
        MentionSpamTriggerMetadata(None),
    )


def test__MentionSpamTriggerMetadata__from_data__3():
    """
    Tests whether ``MentionSpamTriggerMetadata``'s `from_data` method works as expected.
    Case: `20`.
    """
    metadata = MentionSpamTriggerMetadata.from_data({
        'mention_total_limit': 20,
    })
    
    vampytest.assert_eq(
        metadata,
        MentionSpamTriggerMetadata(20),
    )
