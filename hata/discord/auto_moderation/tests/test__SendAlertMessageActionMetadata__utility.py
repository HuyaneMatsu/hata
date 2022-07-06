import vampytest

from .. import SendAlertMessageActionMetadata


def test__SendAlertMessageActionMetadata__copy():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s `copy` method works as expected.
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    copy = metadata.copy()
    
    vampytest.assert_eq(metadata, copy)
    vampytest.assert_is_not(metadata, copy)
