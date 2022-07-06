import vampytest

from .. import AutoModerationActionMetadata


def test__AutoModerationActionMetadata__copy():
    """
    Tests whether ``AutoModerationActionMetadata``'s `copy` method works as expected.
    """
    metadata = AutoModerationActionMetadata()
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
