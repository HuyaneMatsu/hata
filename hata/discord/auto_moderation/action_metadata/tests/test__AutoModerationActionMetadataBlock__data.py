import vampytest

from ..block import AutoModerationActionMetadataBlock

from .test__AutoModerationActionMetadataBlock__constructor import _assert_fields_set


def test__AutoModerationActionMetadataBlock__to_data():
    """
    Tests whether ``AutoModerationActionMetadataBlock``'s `to_data` method works as expected.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'custom_message': custom_message,
        },
    )

    
def test__AutoModerationActionMetadataBlock__from_data():
    """
    Tests whether ``AutoModerationActionMetadataBlock``'s `from_data` method works as expected.
    """
    custom_message = 'senya'
    
    data = {
        'custom_message': custom_message,
    }
    
    metadata = AutoModerationActionMetadataBlock.from_data(data)
    _assert_fields_set(metadata)
    vampytest.assert_eq(metadata.custom_message, custom_message)
