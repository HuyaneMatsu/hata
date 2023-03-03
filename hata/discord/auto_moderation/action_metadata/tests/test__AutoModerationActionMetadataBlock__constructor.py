import vampytest

from ..block import AutoModerationActionMetadataBlock


def _assert_fields_set(metadata):
    """
    Asserts whether all attributes are set of the given auto moderation action metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationActionMetadataBlock``
        The action metadata to test.
    """
    vampytest.assert_instance(metadata, AutoModerationActionMetadataBlock)
    vampytest.assert_instance(metadata.custom_message, str, nullable = True)


def test__AutoModerationActionMetadataBlock__new__0():
    """
    Tests whether ``AutoModerationActionMetadataBlock.__new__`` works as intended.
    
    Case: no parameters.
    """
    metadata = AutoModerationActionMetadataBlock()
    _assert_fields_set(metadata)


def test__AutoModerationActionMetadataBlock__new__1():
    """
    Tests whether ``AutoModerationActionMetadataBlock.__new__`` works as intended.
    
    Case: parameters.
    """
    custom_message = 'senya'
    
    metadata = AutoModerationActionMetadataBlock(custom_message)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.custom_message, custom_message)
