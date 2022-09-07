import vampytest

from .. import AutoModerationActionMetadata


def test__AutoModerationActionMetadata__new():
    """
    Tests whether ``AutoModerationActionMetadata.__new__`` returns as expected.
    """
    metadata = AutoModerationActionMetadata()
    
    vampytest.assert_instance(metadata, AutoModerationActionMetadata)
