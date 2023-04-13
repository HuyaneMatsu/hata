import vampytest

from ..base import ChannelMetadataBase

from .test__ChannelMetadataBase__constructor import _assert_fields_set


def test__ChannelMetadataBase__copy():
    """
    Tests whether ``ChannelMetadataBase.copy` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataBase__copy_with__0():
    """
    Tests whether ``ChannelMetadataBase.copy_with` works as intended.
    
    Case: No fields.
    """
    channel_metadata = ChannelMetadataBase()
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataBase.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    channel_metadata = ChannelMetadataBase()
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)
