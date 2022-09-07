import vampytest

from .. import AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerMetadata__to_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `to_data` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    vampytest.assert_eq(
        metadata.to_data(),
        {},
    )


def test__AutoModerationRuleTriggerMetadata__from_data():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `from_data` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadata.from_data({})
    
    vampytest.assert_eq(
        metadata,
        AutoModerationRuleTriggerMetadata(),
    )
