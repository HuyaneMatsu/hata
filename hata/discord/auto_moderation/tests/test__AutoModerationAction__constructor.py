import vampytest

from ...channel import Channel

from .. import AutoModerationAction, AutoModerationActionType, AutoModerationActionMetadataSendAlertMessage, AutoModerationActionMetadataTimeout



def test__AutoModerationAction__new__action_type__0():
    """
    Tests whether the auto moderation action's `action_type` parameter works as expected when passing as
    ``AutoModerationActionType`` instance.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    vampytest.assert_is(action.type, AutoModerationActionType.block_message)


def test__AutoModerationAction__new__action_type__1():
    """
    Tests whether the auto moderation action's `action_type` parameter works as expected when passing as
    `int` instance.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message.value)
    
    vampytest.assert_is(action.type, AutoModerationActionType.block_message)


def test__AutoModerationAction__new__action_type__2():
    """
    Tests whether the auto moderation action's `action_type` parameter drops error when given an invalid type.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationAction('owo')


def test__AutoModerationAction__new__channel__0():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata type.
    """
    action = AutoModerationAction(channel = 0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.send_alert_message)
    vampytest.assert_instance(action.metadata, AutoModerationActionMetadataSendAlertMessage)


def test__AutoModerationAction__new__channel__1():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `0`.
    """
    action = AutoModerationAction(channel = 0)
    vampytest.assert_eq(action.metadata.channel_id, 0)


def test__AutoModerationAction__new__channel__2():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `None`.
    """
    action = AutoModerationAction(channel = None)
    vampytest.assert_eq(action.metadata.channel_id, 0)


def test__AutoModerationAction__new__channel__3():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `int`.
    """
    action = AutoModerationAction(channel = 69)
    
    vampytest.assert_eq(action.metadata.channel_id, 69)


def test__AutoModerationAction__new__channel__4():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing ``Channel``.
    """
    action = AutoModerationAction(channel = Channel.precreate(69))
    
    vampytest.assert_eq(action.metadata.channel_id, 69)


def test__AutoModerationAction__new__duration__0():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata type.
    """
    action = AutoModerationAction(duration=0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.timeout)
    vampytest.assert_instance(action.metadata, AutoModerationActionMetadataTimeout)


def test__AutoModerationAction__new__duration__1():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `0`.
    """
    action = AutoModerationAction(duration=0)
    
    vampytest.assert_eq(action.metadata.duration, 0)


def test__AutoModerationAction__new__duration__2():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `None`.
    """
    action = AutoModerationAction(duration=None)
    
    vampytest.assert_eq(action.metadata.duration, 0)


def test__AutoModerationAction__new__duration__3():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `int`.
    """
    action = AutoModerationAction(duration=69)
    
    vampytest.assert_eq(action.metadata.duration, 69)


def test__AutoModerationAction__new__duration__4():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `float`.
    """
    action = AutoModerationAction(duration=69.0)
    
    vampytest.assert_eq(action.metadata.duration, 69)


def test__AutoModerationAction__new__metadata_type_match__0():
    """
    Tests whether the auto moderation action's type & type specific keyword parameters are accepted at the same time.
    Case: `send_alert_message`.
    """
    action = AutoModerationAction(AutoModerationActionType.send_alert_message, channel = 0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.send_alert_message)


def test__AutoModerationAction__new__metadata_type_match__1():
    """
    Tests whether the auto moderation action's type & type specific keyword parameters are accepted at the same time.
    Case: `timeout`.
    """
    action = AutoModerationAction(AutoModerationActionType.timeout, duration=0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.timeout)


def test__AutoModerationAction__new__metadata_type_contradiction__0():
    """
    Tests whether the auto moderation action's type & different type specific keyword parameters are not accepted
    at the same time.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationAction(AutoModerationActionType.timeout, channel = 0)


def test__AutoModerationAction__new__metadata_type_contradiction__1():
    """
    Tests whether the auto moderation action's two type specific parameters are not accepted at the same.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationAction(channel = 0, duration=0)
