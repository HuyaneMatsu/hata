import vampytest

from ..alert_message import AutoModerationActionMetadataSendAlertMessage


def test__AutoModerationActionMetadataSendAlertMessage__eq():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__eq__` works as intended.
    """
    channel_id = 202211150000
    
    keyword_parameters = {
        'channel_id': channel_id,
    }
    
    metadata = AutoModerationActionMetadataSendAlertMessage(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('channel_id', 202211150001),
    ):
        test_metadata = AutoModerationActionMetadataSendAlertMessage(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)


def test__AutoModerationActionMetadataSendAlertMessage__hash():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__hash__` works as intended.
    """
    channel_id = 202211150002
    
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id)
    
    vampytest.assert_instance(hash(metadata), int)


def test__AutoModerationActionMetadataSendAlertMessage__repr():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__repr__` works as intended.
    """
    channel_id = 202211150003
    
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id)
    
    vampytest.assert_instance(repr(metadata), str)
