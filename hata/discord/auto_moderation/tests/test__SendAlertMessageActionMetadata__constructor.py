import vampytest

from ...channel import Channel

from .. import SendAlertMessageActionMetadata


def test__SendAlertMessageActionMetadata__new__0():
    """
    Tests whether ``SendAlertMessageActionMetadata.__new__`` returns as expected.
    """
    metadata = SendAlertMessageActionMetadata(0)
    
    vampytest.assert_instance(metadata, SendAlertMessageActionMetadata)


def test__SendAlertMessageActionMetadata__new__1():
    """
    Tests whether ``SendAlertMessageActionMetadata.__new__`` works as expected.
    
    Case: Passing parameter as `None`
    """
    metadata = SendAlertMessageActionMetadata(None)
    
    vampytest.assert_eq(metadata.channel_id, 0)


def test__SendAlertMessageActionMetadata__new__2():
    """
    Tests whether ``SendAlertMessageActionMetadata.__new__`` works as expected.
    
    Case: Passing parameter as `int`
    """
    metadata = SendAlertMessageActionMetadata(69)
    
    vampytest.assert_eq(metadata.channel_id, 69)


def test__SendAlertMessageActionMetadata__new__3():
    """
    Tests whether ``SendAlertMessageActionMetadata.__new__`` works as expected.
    
    Case: Passing parameter as ``Channel``
    """
    metadata = SendAlertMessageActionMetadata(Channel.precreate(69))
    
    vampytest.assert_eq(metadata.channel_id, 69)
