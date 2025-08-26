import vampytest

from ....activity import Activity, ActivityType

from ...activity_change import ActivityChange
from ...activity_update import ActivityUpdate
from ...status_by_platform import Status, StatusByPlatform

from ..client_user_presence_base import ClientUserPBase


def test__ClientUserPBase__from_data():
    """
    Tests whether ``ClientUserPBase.from_data`` works as intended.
    """
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        ClientUserPBase.from_data(data, None, 0)


def test__ClientUserPBase__update_presence():
    """
    Tests whether ``ClientUserPBase._update_presence`` works as intended.
    """
    activities = [
        Activity('orin dance', activity_id = 202302080000, activity_type = ActivityType.playing),
        Activity('okuu dance', activity_id = 202302080001, activity_type = ActivityType.playing),
    ]
    status = Status.online
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    user = ClientUserPBase()
    
    data = {
        'activities': [activity.to_data(defaults = True, include_internals = True) for activity in activities],
        'status': status.value,
        'client_status': status_by_platform.to_data(),
    }
    
    user._update_presence(data)
    
    vampytest.assert_eq(user.activities, activities)
    vampytest.assert_is(user.status, status)
    vampytest.assert_eq(user.status_by_platform, status_by_platform)
    


def test__ClientUserPBase__difference_update_presence():
    """
    Tests whether ``ClientUserPBase._difference_update_presence`` works as intended.
    """
    old_activities = [
        Activity('orin dance', activity_id = 202302080002, activity_type = ActivityType.playing),
        Activity('okuu dance', activity_id = 202302080003, activity_type = ActivityType.playing),
    ]
    old_status = Status.online
    old_status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    new_activities = [
        Activity('okuu lay', activity_id = 202302080003, activity_type = ActivityType.playing),
        Activity('satori dance', activity_id = 202302080004, activity_type = ActivityType.playing),
    ]
    new_status = Status.idle
    new_status_by_platform = StatusByPlatform(
        desktop = Status.online,
    )
    
    user = ClientUserPBase(
        activities = old_activities,
        status = old_status,
        status_by_platform = old_status_by_platform.copy(),
    )
    
    data = {
        'activities': [activity.to_data(defaults = True, include_internals = True) for activity in new_activities],
        'status': new_status.value,
        'client_status': new_status_by_platform.to_data(),
    }
    
    expected_output = {
        'activities': ActivityChange(
            added = [Activity('satori dance', activity_id = 202302080004, activity_type = ActivityType.playing)],
            removed = [Activity('orin dance', activity_id = 202302080002, activity_type = ActivityType.playing)],
            updated = [
                ActivityUpdate(
                    activity = Activity('okuu lay', activity_id = 202302080003, activity_type = ActivityType.playing),
                    old_attributes = {'name': 'okuu dance'}
                ),
            ],
        ),
        'status': old_status,
        'status_by_platform': old_status_by_platform,
    }
    
    output = user._difference_update_presence(data)
    
    vampytest.assert_eq(output, expected_output)
    
    vampytest.assert_eq(user.activities, new_activities)
    vampytest.assert_is(user.status, new_status)
    vampytest.assert_eq(user.status_by_platform, new_status_by_platform)
    
