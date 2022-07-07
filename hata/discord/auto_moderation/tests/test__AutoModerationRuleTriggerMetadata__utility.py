import vampytest

from .. import AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerMetadata__copy():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s `copy` method works as expected.
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
