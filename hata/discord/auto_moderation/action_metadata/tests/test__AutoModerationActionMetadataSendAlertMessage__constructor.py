import vampytest

from ..alert_message import AutoModerationActionMetadataSendAlertMessage


def _assert_fields_set(metadata):
    """
    Asserts whether all attributes are set of the given auto moderation action metadata.
    
    Parameters
    ----------
    metadata : ``AutoModerationActionMetadataSendAlertMessage``
        The action metadata to test.
    """
    vampytest.assert_instance(metadata, AutoModerationActionMetadataSendAlertMessage)
    vampytest.assert_instance(metadata.channel_id, int)


def test__AutoModerationActionMetadataSendAlertMessage__new__0():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` works as expected.
    
    Case: No parameters given
    """
    metadata = AutoModerationActionMetadataSendAlertMessage()
    _assert_fields_set(metadata)


def test__AutoModerationActionMetadataSendAlertMessage__new__1():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` works as expected.
    
    Case: Parameters given
    """
    channel_id = 202211130001
    
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id = channel_id)
    
    _assert_fields_set(metadata)
    vampytest.assert_eq(metadata.channel_id, channel_id)
