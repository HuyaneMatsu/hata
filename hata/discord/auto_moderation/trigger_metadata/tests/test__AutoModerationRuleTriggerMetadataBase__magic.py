import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataBase


def test__AutoModerationRuleTriggerMetadataBase__eq__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationRuleTriggerMetadataBase(),
        AutoModerationRuleTriggerMetadataBase(),
    )


def test__AutoModerationRuleTriggerMetadataBase__eq__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRuleTriggerMetadataBase(),
        0,
    )


def test__AutoModerationRuleTriggerMetadataBase__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `__hash__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataBase__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `__repr__` method works as intended
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(repr(metadata), str)
