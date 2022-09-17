import vampytest

from .. import AutoModerationActionMetadataBase


def test__AutoModerationActionMetadataBase__new():
    """
    Tests whether ``AutoModerationActionMetadataBase.__new__`` returns as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(metadata, AutoModerationActionMetadataBase)
