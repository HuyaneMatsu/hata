import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase

from .test__AutoModerationRuleTriggerMetadataBase__constructor import _assert_is_every_attribute_set


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
    data = {}
    
    metadata = AutoModerationRuleTriggerMetadataBase.from_data(data)
    _assert_is_every_attribute_set(metadata)
