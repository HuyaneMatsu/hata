import vampytest

from .. import ChannelMetadataBase


def test__ChannelMetadataBase__new():
    """
    Tests whether ``ChannelMetadataBase.__new__`` works as intended.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataBase(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataBase__create_empty():
    """
    Tests whether ``ChannelMetadataBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataBase._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)


def test__ChannelMetadataBase__precreate():
    """
    Tests whether ``ChannelMetadataBase.precreate`` works as intended.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataBase.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)
    vampytest.assert_eq(keyword_parameters, {})
