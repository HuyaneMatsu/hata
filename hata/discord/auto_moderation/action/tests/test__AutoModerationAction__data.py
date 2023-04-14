import vampytest

from ..action import AutoModerationAction
from ..preinstanced import AutoModerationActionType

from .test__AutoModerationAction__constructor import _assert_fields_set


def test__AutoModerationAction__from_data__timeout():
    """
    Tests whether ``AutoModerationAction.from_data`` works as intended.
    """
    duration = 69
    
    data = {
        'type': AutoModerationActionType.timeout.value,
        'metadata': {
            'duration_seconds': duration,
        },
    }
    
    action = AutoModerationAction.from_data(data)
    _assert_fields_set(action)
    
    vampytest.assert_eq(action.duration, duration)


def test__AutoModerationAction__to_data():
    """
    Tests whether ``AutoModerationAction.to_data`` works as intended.
    """
    duration = 69
    
    action = AutoModerationAction(duration = duration)
    
    vampytest.assert_eq(
        action.to_data(),
        {
            'type': AutoModerationActionType.timeout.value,
            'metadata': {
                'duration_seconds': duration,
            },
        }
    )
