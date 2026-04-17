import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase


def test__AutoModerationRuleTriggerMetadataBase__eq():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.__eq__`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())


def test__AutoModerationRuleTriggerMetadataBase__hash():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.__eq__`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationRuleTriggerMetadataBase__repr():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataBase.__eq__`` works as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataBase()
    
    vampytest.assert_instance(repr(metadata), str)
