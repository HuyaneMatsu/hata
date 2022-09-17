import vampytest

from .. import ChannelMetadataBase


def test__ChannelMetadataBase__from_data():
    """
    Tests whether ``ChannelMetadataBase.from_data` works as intended.
    """
    channel_metadata = ChannelMetadataBase.from_data({})
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)


def test__ChannelMetadataBase__to_data():
    """
    Tests whether ``ChannelMetadataBase.to_data`` works as intended.
    """
    channel_metadata = ChannelMetadataBase({})
    
    data = channel_metadata.to_data()
    
    vampytest.assert_eq(data, {})


def test__ChannelMetadataBase__update_attributes():
    """
    Tests whether ``ChannelMetadataBase._update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataBase({})
    
    channel_metadata._update_attributes({})


def test__ChannelMetadataBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataBase._difference_update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataBase({})
    
    old_attributes = channel_metadata._difference_update_attributes({})


def test__ChannelMetadataBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataBase._from_partial_data`` works as intended.
    """
    channel_metadata = ChannelMetadataBase._from_partial_data({})
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataBase)
