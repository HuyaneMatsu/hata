import vampytest

from .. import AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerMetadata__constructor_0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata``'s constructor returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadata)
