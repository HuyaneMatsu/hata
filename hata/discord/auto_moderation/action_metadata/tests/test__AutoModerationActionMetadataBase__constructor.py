import vampytest

from ..base import AutoModerationActionMetadataBase


def _check_is_all_attribute_set(metadata):
    """
    Asserts whether all attributes are set of the given auto moderation action metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationActionMetadataBase``
        The action metadata to test.
    """
    vampytest.assert_instance(metadata, AutoModerationActionMetadataBase)


def test__AutoModerationActionMetadataBase__new():
    """
    Tests whether ``AutoModerationActionMetadataBase.__new__`` returns as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    _check_is_all_attribute_set(metadata)
