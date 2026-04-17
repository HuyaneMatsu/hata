import vampytest

from ..base import ChannelMetadataBase


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)


def test__ChannelMetadataBase__new():
    """
    Tests whether ``ChannelMetadataBase.__new__`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataBase__from_keyword_parameters():
    """
    Tests whether ``ChannelMetadataBase.from_keyword_parameters`` works as intended.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataBase__create_empty():
    """
    Tests whether ``ChannelMetadataBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataBase._create_empty()
    _assert_fields_set(channel_metadata)
