import vampytest

from ..timeout import AutoModerationActionMetadataTimeout

from .test__AutoModerationActionMetadataTimeout__constructor import _check_is_all_attribute_set


def test__AutoModerationActionMetadataTimeout__copy():
    """
    Tests whether ``AutoModerationActionMetadataTimeout``'s `copy` method works as expected.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    
    copy = metadata.copy()
    _check_is_all_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataTimeout__copy_with__0():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.copy_with method works as expected.
    
    Case: No fields given.
    """
    duration = 69
    
    metadata = AutoModerationActionMetadataTimeout(duration)
    
    copy = metadata.copy_with()
    _check_is_all_attribute_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataTimeout__copy_with__1():
    """
    Tests whether ``AutoModerationActionMetadataTimeout.copy_with method works as expected.
    
    Case: All fields given.
    """
    old_duration = 69
    new_duration = 420
    
    metadata = AutoModerationActionMetadataTimeout(old_duration)
    
    copy = metadata.copy_with(
        duration = new_duration,
    )
    _check_is_all_attribute_set(copy)
    
    vampytest.assert_eq(copy.duration, new_duration)
