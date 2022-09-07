import vampytest

from .. import AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerMetadata__new():
    """
    Tests whether ``AutoModerationRuleTriggerMetadata.__new__`` returns as expected.
    """
    metadata = AutoModerationRuleTriggerMetadata()
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadata)
