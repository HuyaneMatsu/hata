import vampytest

from ..base import AutoModerationActionMetadataBase

from .test__AutoModerationActionMetadataBase__constructor import _check_is_all_attribute_set


def test__AutoModerationActionMetadataBase__copy():
    """
    Tests whether ``AutoModerationActionMetadataBase``'s `copy` method works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    copy = metadata.copy()
    _check_is_all_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataBase__copy_with():
    """
    Tests whether ``AutoModerationActionMetadataBase.copy_with`` works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    copy = metadata.copy_with()
    _check_is_all_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataBase__placeholders():
    """
    Tests whether ``AutoModerationActionMetadataBase``'s placeholders works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_instance(metadata.channel_id, int)
    vampytest.assert_instance(metadata.duration, int)


def test__AutoModerationActionMetadataBase__channel():
    """
    Tests whether ``AutoModerationActionMetadataBase.channel`` works as expected.
    """
    metadata = AutoModerationActionMetadataBase()
    
    vampytest.assert_is(metadata.channel, None)
