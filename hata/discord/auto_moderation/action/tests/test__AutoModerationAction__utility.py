import vampytest

from ....channel import Channel

from ..action import AutoModerationAction

from .test__AutoModerationAction__constructor import _check_is_every_attribute_set


def test__AutoModerationAction__copy():
    """
    Tests whether ``AutoModerationAction.copy`` works as intended.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    
    copy = action.copy()
    
    _check_is_every_attribute_set(copy)
    
    vampytest.assert_eq(action, copy)
    vampytest.assert_not_is(action, copy)


def test__AutoModerationAction__copy_with__0():
    """
    Tests whether ``AutoModerationAction.copy`` works as intended.
    
    Case: No fields.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    
    copy = action.copy_with()
    
    _check_is_every_attribute_set(copy)
    
    vampytest.assert_eq(action, copy)
    vampytest.assert_not_is(action, copy)


def test__AutoModerationAction__copy_with__1():
    """
    Tests whether ``AutoModerationAction.copy`` works as intended.
    
    Case: No stuffed.
    """
    duration = 69
    channel_id = 20221115007
    
    action = AutoModerationAction(duration = duration)
    
    copy = action.copy_with(
        channel_id = channel_id,
    )
    
    _check_is_every_attribute_set(copy)
    
    vampytest.assert_not_is(action, copy)
    vampytest.assert_eq(copy.channel_id, channel_id)


def test__AutoModerationAction__proxies():
    """
    Tests whether ``AutoModerationAction``'s proxies work as intended. works as intended.
    """
    action = AutoModerationAction()
    
    vampytest.assert_instance(action.channel_id, int)
    vampytest.assert_instance(action.duration, int)
    vampytest.assert_instance(action.custom_message, str, nullable = True)


def test__AutoModerationAction__proxy__duration():
    """
    Tests whether ``AutoModerationAction.duration`` works as intended.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    vampytest.assert_eq(action.duration, duration)


def test__AutoModerationAction__proxy__channel_id():
    """
    Tests whether ``AutoModerationAction.channel_id`` works as intended.
    """
    channel_id = 20221115008
    
    action = AutoModerationAction(channel_id = channel_id)
    vampytest.assert_eq(action.channel_id, channel_id)


def test__AutoModerationAction__proxy__channel():
    """
    Tests whether ``AutoModerationAction.channel`` works as intended.
    """
    for channel_id, expected_channel in (
        (0, None),
        (20221115009, Channel.precreate(20221115009)),
    ):
        action = AutoModerationAction(channel_id = channel_id)
        vampytest.assert_is(action.channel, expected_channel)


def test__AutoModerationAction__proxy__custom_message():
    """
    Tests whether ``AutoModerationAction.custom_message`` works as intended.
    """
    custom_message = 'orin'
    
    action = AutoModerationAction(custom_message = custom_message)
    vampytest.assert_eq(action.custom_message, custom_message)
