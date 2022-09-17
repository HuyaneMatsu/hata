import vampytest

from ....channel import Channel

from .. import AutoModerationActionMetadataTimeout


def test__AutoModerationActionMetadataTimeout__new__0():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s constructor returns as expected.
    """
    metadata = AutoModerationActionMetadataTimeout(0)
    
    vampytest.assert_instance(metadata, AutoModerationActionMetadataTimeout)


def test__AutoModerationActionMetadataTimeout__new__1():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s constructor works as expected.
    Passing parameter as `None`
    """
    metadata = AutoModerationActionMetadataTimeout(None)
    
    vampytest.assert_eq(metadata.duration, 0)


def test__AutoModerationActionMetadataTimeout__new__2():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s constructor works as expected.
    Passing parameter as `int`
    """
    metadata = AutoModerationActionMetadataTimeout(69)
    
    vampytest.assert_eq(metadata.duration, 69)


def test__AutoModerationActionMetadataTimeout__new__3():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s constructor works as expected.
    Passing parameter as ``float``
    """
    metadata = AutoModerationActionMetadataTimeout(69.0)
    
    vampytest.assert_eq(metadata.duration, 69)
