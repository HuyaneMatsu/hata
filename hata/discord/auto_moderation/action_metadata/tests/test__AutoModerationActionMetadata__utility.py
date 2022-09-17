import vampytest

from .. import AutoModerationActionMetadataBase


def test__AutoModerationActionMetadataBase__copy():
    """
    Tests whether ``AutoModerationActionMetadataBase``'s `copy` method works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
