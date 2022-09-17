import vampytest

from .. import AutoModerationActionMetadataBase


def test__AutoModerationActionMetadataBase__eq__0():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__eq__` method works as expected.
    """
    vampytest.assert_eq(
        AutoModerationActionMetadataBase(),
        AutoModerationActionMetadataBase(),
    )


def test__AutoModerationActionMetadataBase__eq__1():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationActionMetadataBase(),
        0,
    )


def test__AutoModerationActionMetadataBase__hash():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__hash__` method works as intended
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataBase__repr():
    """
    Tests whether ``AutoModerationActionMetadata``'s `__repr__` method works as intended
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(repr(metadata), str)
