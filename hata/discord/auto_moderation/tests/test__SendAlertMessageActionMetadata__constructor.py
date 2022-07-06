import vampytest

from ...channel import Channel

from .. import SendAlertMessageActionMetadata


def test__SendAlertMessageActionMetadata__constructor_0():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s constructor returns as expected.
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    vampytest.assert_instance(metadata, SendAlertMessageActionMetadata)


def test__SendAlertMessageActionMetadata__constructor_1():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s constructor works as expected.
    Passing parameter as `None`
    """
    metadata = SendAlertMessageActionMetadata(None)
    
    vampytest.assert_eq(metadata.channel_id, 0)


def test__SendAlertMessageActionMetadata__constructor_2():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s constructor works as expected.
    Passing parameter as `int`
    """
    metadata = SendAlertMessageActionMetadata(69)
    
    vampytest.assert_eq(metadata.channel_id, 69)


def test__SendAlertMessageActionMetadata__constructor_3():
    """
    Tests whether ``SendAlertMessageActionMetadata``'s constructor works as expected.
    Passing parameter as ``Channel``
    """
    metadata = SendAlertMessageActionMetadata(Channel.precreate(69))
    
    vampytest.assert_eq(metadata.channel_id, 69)
