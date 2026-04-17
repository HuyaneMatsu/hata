import vampytest

from ..action import AutoModerationAction


def test__AutoModerationAction__eq__0():
    """
    Tests whether ``AutoModerationAction.__eq__`` works as intended.
    """
    duration = 69
    channel_id = 202211150006
    
    action = AutoModerationAction(duration = duration)
    vampytest.assert_eq(action, action)
    vampytest.assert_ne(action, object())
    
    test_action = AutoModerationAction(channel_id = channel_id)
    vampytest.assert_ne(action, test_action)


def test__AutoModerationAction__hash():
    """
    Tests whether ``AutoModerationAction.__eq__`` works as intended.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    
    vampytest.assert_instance(hash(action), int)


def test__AutoModerationAction__repr():
    """
    Tests whether ``AutoModerationAction.__eq__`` works as intended.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    
    vampytest.assert_instance(repr(action), str)
