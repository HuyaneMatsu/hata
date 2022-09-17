import vampytest

from .. import AutoModerationActionMetadataTimeout


def test__AutoModerationActionMetadataTimeout__copy():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `copy` method works as expected.
    """
    metadata = AutoModerationActionMetadataTimeout(0)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
