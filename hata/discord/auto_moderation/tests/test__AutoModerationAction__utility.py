import vampytest

from .. import AutoModerationAction, AutoModerationActionType


def test__AutoModerationAction__copy__0():
    """
    Tests whether the auto moderation action's `copy` method works.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    copy = action.copy()
    
    vampytest.assert_eq(action, copy)
    vampytest.assert_not_is(action, copy)


def test__AutoModerationAction__copy__1():
    """
    Tests whether the auto moderation action's `copy` method deep copies.
    """
    action = AutoModerationAction(channel = 69)
    
    copy = action.copy()
    
    vampytest.assert_eq(action.metadata, copy.metadata)
    vampytest.assert_not_is(action.metadata, copy.metadata)



def test__AutoModerationAction__copy_with__0():
    """
    Tests whether the auto moderation action's `copy_with` method works.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    copy = action.copy_with()
    
    vampytest.assert_eq(action, copy)
    vampytest.assert_not_is(action, copy)


def test__AutoModerationAction__copy_with__1():
    """
    Tests whether the auto moderation action's `copy_with` method deep copies.
    """
    action = AutoModerationAction(channel = 69)
    
    copy = action.copy_with()
    
    vampytest.assert_eq(action.metadata, copy.metadata)
    vampytest.assert_not_is(action.metadata, copy.metadata)


def test__AutoModerationAction__copy_with__2():
    """
    Tests whether the auto moderation action's `copy_with` method copies with different parameters. Same type.
    """
    action = AutoModerationAction(channel = 69)
    
    copy = action.copy_with(channel = 68)
    
    vampytest.assert_is(action.type, copy.type)
    vampytest.assert_ne(action, copy)
    vampytest.assert_eq(copy.metadata.channel_id, 68)


def test__AutoModerationAction__copy_with__3():
    """
    Tests whether the auto moderation action's `copy_with` method copies with different parameters. Different type.
    """
    action = AutoModerationAction(channel = 69)
    
    copy = action.copy_with(duration=69)
    
    vampytest.assert_is_not(action.type, copy.type)
    vampytest.assert_ne(action, copy)
