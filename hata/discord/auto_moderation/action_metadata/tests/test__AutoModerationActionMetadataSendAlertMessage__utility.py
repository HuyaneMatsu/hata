import vampytest

from .. import AutoModerationActionMetadataSendAlertMessage


def test__AutoModerationActionMetadataSendAlertMessage__copy():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `copy` method works as expected.
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(0)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
