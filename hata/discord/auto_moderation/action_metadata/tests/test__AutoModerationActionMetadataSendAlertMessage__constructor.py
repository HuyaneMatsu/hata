import vampytest

from ....channel import Channel

from .. import AutoModerationActionMetadataSendAlertMessage


def test__AutoModerationActionMetadataSendAlertMessage__new__0():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` returns as expected.
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(0)
    
    vampytest.assert_instance(metadata, AutoModerationActionMetadataSendAlertMessage)


def test__AutoModerationActionMetadataSendAlertMessage__new__1():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` works as expected.
    
    Case: Passing parameter as `None`
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(None)
    
    vampytest.assert_eq(metadata.channel_id, 0)


def test__AutoModerationActionMetadataSendAlertMessage__new__2():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` works as expected.
    
    Case: Passing parameter as `int`
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(69)
    
    vampytest.assert_eq(metadata.channel_id, 69)


def test__AutoModerationActionMetadataSendAlertMessage__new__3():
    """
    Tests whether ``AutoModerationActionMetadataSendAlertMessage.__new__`` works as expected.
    
    Case: Passing parameter as ``Channel``
    """
    metadata = AutoModerationActionMetadataSendAlertMessage(Channel.precreate(69))
    
    vampytest.assert_eq(metadata.channel_id, 69)
