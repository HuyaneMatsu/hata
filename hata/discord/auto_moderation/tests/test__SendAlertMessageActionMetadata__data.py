import vampytest

from .. import SendAlertMessageActionMetadata


def test__SendAlertMessageActionMetadata__to_data():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `to_data` method works as expected.
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'channel_id': 0,
        },
    )

    
def test__SendAlertMessageActionMetadata__from_data():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `from_data` method works as expected.
    """
    metadata = SendAlertMessageActionMetadata.from_data({
        'channel_id': '0',
    })
    
    vampytest.assert_eq(
        metadata,
        SendAlertMessageActionMetadata(0),
    )
