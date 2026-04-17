import vampytest

from ..alert_message import AutoModerationActionMetadataSendAlertMessage

from .test__AutoModerationActionMetadataSendAlertMessage__constructor import _assert_fields_set


def test__AutoModerationActionMetadataSendAlertMessage__copy():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.copy`` works as expected.
    """
    channel_id = 202211130004
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id)
    
    copy = metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataSendAlertMessage__copy_with__0():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.copy-with`` works as expected.
    
    Case: no fields given.
    """
    channel_id = 202211130005
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id)
    
    copy = metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)


def test__AutoModerationActionMetadataSendAlertMessage__copy_with__1():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.copy-with`` works as expected.
    
    Case: no fields given.
    """
    old_channel_id = 202211130006
    new_channel_id = 202211130007
    
    metadata = AutoModerationActionMetadataSendAlertMessage(old_channel_id)
    
    copy = metadata.copy_with(channel_id = new_channel_id)
    
    _assert_fields_set(copy)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
