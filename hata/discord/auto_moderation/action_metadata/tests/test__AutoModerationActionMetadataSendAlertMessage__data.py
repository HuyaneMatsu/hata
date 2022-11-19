import vampytest

from ..alert_message import AutoModerationActionMetadataSendAlertMessage

from .test__AutoModerationActionMetadataSendAlertMessage__constructor import _check_is_all_attribute_set


def test__AutoModerationActionMetadataSendAlertMessage__to_data():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.to_data`` works as expected.
    """
    channel_id = 202211130002
    
    metadata = AutoModerationActionMetadataSendAlertMessage(channel_id)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'channel_id': str(channel_id),
        },
    )

    
def test__AutoModerationActionMetadataSendAlertMessage__from_data():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `from_data` method works as expected.
    """
    channel_id = 202211130003
    
    data = {
        'channel_id': str(channel_id),
    }
    
    metadata = AutoModerationActionMetadataSendAlertMessage.from_data(data)
    
    _check_is_all_attribute_set(metadata)
    vampytest.assert_eq(metadata.channel_id, channel_id)
