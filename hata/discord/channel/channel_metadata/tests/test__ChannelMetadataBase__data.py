import vampytest

from ..base import ChannelMetadataBase

from .test__ChannelMetadataBase__constructor import _assert_fields_set

def test__ChannelMetadataBase__from_data():
    """
    Tests whether ``ChannelMetadataBase.from_data` works as intended.
    """
    channel_metadata = ChannelMetadataBase.from_data({})
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataBase__to_data():
    """
    Tests whether ``ChannelMetadataBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    channel_metadata = ChannelMetadataBase()
    
    expected_output = {}
    
    vampytest.assert_eq(
        channel_metadata.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ChannelMetadataBase__update_attributes():
    """
    Tests whether ``ChannelMetadataBase._update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    channel_metadata._update_attributes({})


def test__ChannelMetadataBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataBase._difference_update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    old_attributes = channel_metadata._difference_update_attributes({})
    vampytest.assert_eq(old_attributes, {})


def test__ChannelMetadataBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataBase._from_partial_data`` works as intended.
    """
    channel_metadata = ChannelMetadataBase._from_partial_data({})
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataBase__update_status():
    """
    Tests whether ``ChannelMetadataBase._update_status`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    channel_metadata._update_status({})


def test__ChannelMetadataBase__difference_update_status():
    """
    Tests whether ``ChannelMetadataBase._difference_update_status`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    old_attributes = channel_metadata._difference_update_status({})
    vampytest.assert_eq(old_attributes, {})


def test__ChannelMetadataBase__update_voice_engaged_since():
    """
    Tests whether ``ChannelMetadataBase._update_voice_engaged_since`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    channel_metadata._update_voice_engaged_since({})


def test__ChannelMetadataBase__difference_update_voice_engaged_since():
    """
    Tests whether ``ChannelMetadataBase._difference_update_voice_engaged_since`` works as intended.
    """
    channel_metadata = ChannelMetadataBase()
    
    old_attributes = channel_metadata._difference_update_voice_engaged_since({})
    vampytest.assert_eq(old_attributes, {})
