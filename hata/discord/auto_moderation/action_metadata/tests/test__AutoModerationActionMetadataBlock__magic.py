import vampytest

from ..block import AutoModerationActionMetadataBlock


def test__AutoModerationActionMetadataBlock__eq__0():
    """
    Tests whether ``AutoModerationActionMetadataBlock.__eq__` works as intended.
    """
    custom_message = 'senya'
    
    keyword_parameters = {
        'custom_message': custom_message,
    }
    
    metadata = AutoModerationActionMetadataBlock(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('custom_message', 'hijiri'),
    ):
        test_metadata = AutoModerationActionMetadataBlock(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)


def test__AutoModerationActionMetadataBlock__hash():
    """
    Tests whether ``AutoModerationActionMetadataBlock.__hash__` works as intended.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataBlock__repr():
    """
    Tests whether ``AutoModerationActionMetadataBlock.__repr__` works as intended.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    
    vampytest.assert_instance(repr(metadata), str)
