import vampytest

from .. import ChannelMetadataBase


def test__ChannelMetadataBase__repr():
    """
    Tests whether ``.ChannelMetadataBase.__repr__`` works as intended.
    """
    channel_metadata = ChannelMetadataBase({})
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataBase__hash():
    """
    Tests whether ``.ChannelMetadataBase.__hash__`` works as intended.
    """
    channel_metadata = ChannelMetadataBase({})
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataBase__eq():
    """
    Tests whether ``.ChannelMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
    ):
        test_channel_metadata = ChannelMetadataBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
