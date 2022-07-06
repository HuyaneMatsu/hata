import vampytest

from .. import AutoModerationAction, AutoModerationActionType


def test__AutoModerationAction__eq_0():
    """
    Tests whether the auto moderation action's `__eq__` method works.
    """
    vampytest.assert_eq(
        AutoModerationAction(AutoModerationActionType.block_message),
        AutoModerationAction(AutoModerationActionType.block_message),
    )
    
    vampytest.assert_eq(
        AutoModerationAction(AutoModerationActionType.timeout),
        AutoModerationAction(AutoModerationActionType.timeout),
    )
    
    vampytest.assert_eq(
        AutoModerationAction(duration=60),
        AutoModerationAction(duration=60),
    )
    
    vampytest.assert_not_eq(
        AutoModerationAction(duration=60),
        AutoModerationAction(duration=59),
    )
    
    vampytest.assert_not_eq(
        AutoModerationAction(duration=60),
        AutoModerationAction(channel=59),
    )
    
    vampytest.assert_not_eq(
        AutoModerationAction(AutoModerationActionType.block_message),
        AutoModerationAction(channel=59),
    )


def test__AutoModerationAction__eq_1():
    """
    Tests whether the auto moderation action's `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationAction(AutoModerationActionType.block_message),
        1337,
    )


def test__AutoModerationAction__hash():
    """
    Tests whether the auto moderation action's `__hash__` method works.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    vampytest.assert_instance(hash(action), int)


def test__AutoModerationAction__repr():
    """
    Tests whether the auto moderation action's `__repr__` method works.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    vampytest.assert_instance(repr(action), str)
