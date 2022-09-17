import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataMentionSpam


def test__AutoModerationRuleTriggerMetadataMentionSpam__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadataMentionSpam(None),
        AutoModerationRuleTriggerMetadataMentionSpam(None),
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__eq__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataMentionSpam(None),
        0,
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__not_eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `__eq__` method works as expected when passing
    objects with different values.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataMentionSpam(None),
        AutoModerationRuleTriggerMetadataMentionSpam(20),
    )


def test__AutoModerationRuleTriggerMetadataMentionSpam__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `__hash__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataMentionSpam__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataMentionSpam``'s `__repr__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(None)
    
    vampytest.assert_instance(repr(metadata), str)
