import vampytest

from ...channel import Channel

from .. import AutoModerationAction, AutoModerationActionType, SendAlertMessageActionMetadata, TimeoutActionMetadata



def test__AutoModerationAction__constructor__action_type_0():
    """
    Tests whether the auto moderation action's `action_type` parameter works as expected when passing as
    ``AutoModerationActionType`` instance.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    vampytest.assert_is(action.type, AutoModerationActionType.block_message)


def test__AutoModerationAction__constructor__action_type_1():
    """
    Tests whether the auto moderation action's `action_type` parameter works as expected when passing as
    `int` instance.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message.value)
    
    vampytest.assert_is(action.type, AutoModerationActionType.block_message)


def test__AutoModerationAction__constructor__action_type_2():
    """
    Tests whether the auto moderation action's `action_type` parameter drops error when given an invalid type.
    """
    
    with vampytest.assert_raises(TypeError):
        AutoModerationAction('owo')


def test__AutoModerationAction__constructor__channel_0():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata type.
    """
    action = AutoModerationAction(channel=0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.send_alert_message)
    vampytest.assert_instance(action.metadata, SendAlertMessageActionMetadata)


def test__AutoModerationAction__constructor__channel_1():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `0`.
    """
    action = AutoModerationAction(channel=0)
    vampytest.assert_eq(action.metadata.channel_id, 0)


def test__AutoModerationAction__constructor__channel_2():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `None`.
    """
    action = AutoModerationAction(channel=None)
    vampytest.assert_eq(action.metadata.channel_id, 0)


def test__AutoModerationAction__constructor__channel_3():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing `int`.
    """
    action = AutoModerationAction(channel=69)
    
    vampytest.assert_eq(action.metadata.channel_id, 69)


def test__AutoModerationAction__constructor__channel_4():
    """
    Tests whether the auto moderation action's `channel` parameter works as intended.
    Checking metadata value and passing ``Channel``.
    """
    action = AutoModerationAction(channel=Channel.precreate(69))
    
    vampytest.assert_eq(action.metadata.channel_id, 69)



def test__AutoModerationAction__constructor__duration_0():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata type.
    """
    action = AutoModerationAction(duration=0)
    
    vampytest.assert_is(action.type, AutoModerationActionType.timeout)
    vampytest.assert_instance(action.metadata, TimeoutActionMetadata)


def test__AutoModerationAction__constructor__duration_1():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `0`.
    """
    action = AutoModerationAction(duration=0)
    
    vampytest.assert_eq(action.metadata.duration, 0)


def test__AutoModerationAction__constructor__duration_2():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `None`.
    """
    action = AutoModerationAction(duration=None)
    
    vampytest.assert_eq(action.metadata.duration, 0)


def test__AutoModerationAction__constructor__duration_3():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `int`.
    """
    action = AutoModerationAction(duration=69)
    
    vampytest.assert_eq(action.metadata.duration, 69)


def test__AutoModerationAction__constructor__duration_4():
    """
    Tests whether the auto moderation action's `duration` parameter works as intended.
    Checking metadata value and passing `float`.
    """
    action = AutoModerationAction(duration=69.0)
    
    vampytest.assert_eq(action.metadata.duration, 69)


def test__AutoModerationAction__constructor__metadata_type_match_0():
    """
    Tests whether the auto moderation action's type & type specific keyword parameters are accepted at the same time.
    Case: `send_alert_message`.
    """
    action = AutoModerationAction(AutoModerationActionType.send_alert_message, channel=0)
    
    vampytest.assert_eq(action.type, AutoModerationActionType.send_alert_message)


def test__AutoModerationAction__constructor__metadata_type_match_1():
    """
    Tests whether the auto moderation action's type & type specific keyword parameters are accepted at the same time.
    Case: `timeout`.
    """
    action = AutoModerationAction(AutoModerationActionType.timeout, duration=0)
    
    vampytest.assert_eq(action.type, AutoModerationActionType.timeout)


def test__AutoModerationAction__constructor__metadata_type_contradiction():
    """
    Tests whether the auto moderation action's type & different type specific keyword parameters are not accepted
    at the same time.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationAction(AutoModerationActionType.timeout, channel=0)
