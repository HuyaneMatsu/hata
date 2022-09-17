import vampytest

from .. import AutoModerationActionMetadataSendAlertMessage


def test__AutoModerationActionMetadataSendAlertMessage__to_data():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `to_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(0)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'channel_id': 0,
        },
    )

    
def test__AutoModerationActionMetadataSendAlertMessage__from_data():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage``'s `from_data` method works as expected.
    """
    metadata = AutoModerationActionMetadataSendAlertMessage.from_data({
        'channel_id': '0',
    })
    
    vampytest.assert_eq(
        metadata,
        AutoModerationActionMetadataSendAlertMessage(0),
    )
