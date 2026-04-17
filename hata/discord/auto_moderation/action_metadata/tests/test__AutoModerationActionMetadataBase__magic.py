import vampytest

from ..base import AutoModerationActionMetadataBase


def test__AutoModerationActionMetadataBase__eq__0():
    """
    Tests whether ``AutoModerationActionMetadata.__eq__` works as intended.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())


def test__AutoModerationActionMetadataBase__hash():
    """
    Tests whether ``AutoModerationActionMetadata.__hash__` works as intended.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataBase__repr():
    """
    Tests whether ``AutoModerationActionMetadata.__repr__` works as intended.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(repr(metadata), str)
