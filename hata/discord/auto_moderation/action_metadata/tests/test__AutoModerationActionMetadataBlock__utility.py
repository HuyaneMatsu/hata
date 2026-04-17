import vampytest

from ..block import AutoModerationActionMetadataBlock

from .test__AutoModerationActionMetadataBlock__constructor import _assert_fields_set


def test__AutoModerationActionMetadataBlock__copy():
    """
    Tests whether ``AutoModerationActionMetadataBlock``'s `copy` method works as expected.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    
    copy = metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataBlock__copy_with__0():
    """
    Tests whether ``AutoModerationActionMetadataBlock.copy_with method works as expected.
    
    Case: No fields given.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    
    copy = metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataBlock__copy_with__1():
    """
    Tests whether ``AutoModerationActionMetadataBlock.copy_with method works as expected.
    
    Case: All fields given.
    """
    old_custom_message = 'senya'
    new_custom_message = 'hijiri'
    
    metadata = AutoModerationActionMetadataBlock(old_custom_message)
    
    copy = metadata.copy_with(
        custom_message = new_custom_message,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy.custom_message, new_custom_message)
