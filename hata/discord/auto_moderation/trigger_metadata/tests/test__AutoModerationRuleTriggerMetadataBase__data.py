import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataBase


def test__AutoModerationRuleTriggerMetadataBase__to_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `to_data` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq(
        metadata.to_data(),
        {},
    )


def test__AutoModerationRuleTriggerMetadataBase__from_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase``'s `from_data` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadataBase.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadataBase(),
    )
