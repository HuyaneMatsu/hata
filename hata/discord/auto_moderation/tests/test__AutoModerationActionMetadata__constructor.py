import vampytest

from .. import AutoModerationActionMetadata


def test__AutoModerationActionMetadata__constructor_0():
    """
    Tests whether ``AutoModerationActionMetadata``'s constructor returns as expected.
    """
    metadata = AutoModerationActionMetadata()
    
    vampytest.assert_instance(metadata, AutoModerationActionMetadata)
