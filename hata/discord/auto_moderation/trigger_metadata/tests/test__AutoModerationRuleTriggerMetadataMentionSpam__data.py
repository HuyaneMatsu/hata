import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataMentionSpam


def test__AutoModerationRuleTriggerMetadataMentionSpam__to_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `to_data` method works as expected.
    Defining no keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    vampytest.assert_instance(metadata.to_data()['mention_total_limit'], int)


def test__AutoModerationRuleTriggerMetadataMentionSpam__to_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `to_data` method works as expected.
    Defining keyword(s).
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(20)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'mention_total_limit': 20,
        },
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data({
        'mention_total_limit': None,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataMentionSpam(None),
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `from_data` method works as expected.
    Case: *missing*.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataMentionSpam(None),
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `from_data` method works as expected.
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data({
        'mention_total_limit': None,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataMentionSpam(None),
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__from_data__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `from_data` method works as expected.
    Case: `20`.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam.from_data({
        'mention_total_limit': 20,
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataMentionSpam(20),
    )
