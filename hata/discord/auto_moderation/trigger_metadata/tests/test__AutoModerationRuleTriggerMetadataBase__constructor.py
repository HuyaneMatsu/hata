import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataBase


def test__AutoModerationRuleTriggerMetadataBase__new():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.__new__`` returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataBase)
