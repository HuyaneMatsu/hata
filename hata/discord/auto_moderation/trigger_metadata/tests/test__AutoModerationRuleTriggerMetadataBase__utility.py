import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataBase


def test__AutoModerationRuleTriggerMetadataBase__copy():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `copy` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
