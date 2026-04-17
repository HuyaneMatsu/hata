import vampytest

from ...action_metadata import AutoModerationActionMetadataBase

from ..action import AutoModerationAction
from ..preinstanced import AutoModerationActionType


def _assert_fields_set(action):
    """
    Asserts whether every attributes are set of the given action.
    
    Parameters
    ----------
    action : ``AutoModerationAction``
    """
    vampytest.assert_instance(action, AutoModerationAction)
    vampytest.assert_instance(action.type, AutoModerationActionType)
    vampytest.assert_instance(action.metadata, AutoModerationActionMetadataBase)
    

def test__AutoModerationAction__new__0():
    """
    Tests whether ``AutoModerationAction`` works as intended.
    
    Case: No parameters.
    """
    action = AutoModerationAction()
    _assert_fields_set(action)


def test__AutoModerationAction__new__1():
    """
    Tests whether ``AutoModerationAction`` works as intended.
    
    Case: Extra only.
    """
    duration = 69
    action = AutoModerationAction(duration = duration)
    
    vampytest.assert_eq(action.duration, duration)
    vampytest.assert_is(action.type, AutoModerationActionType.timeout)


def test__AutoModerationAction__new__2():
    """
    Tests whether ``AutoModerationAction`` works as intended.
    
    Case: contradiction.
    """
    duration = 69
    
    with vampytest.assert_raises(TypeError):
        AutoModerationAction(AutoModerationActionType.send_alert_message, duration = duration)
