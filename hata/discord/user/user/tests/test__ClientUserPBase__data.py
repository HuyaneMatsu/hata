import vampytest

from ....activity import Activity, ActivityType

from ...activity_change import ActivityChange
from ...activity_update import ActivityUpdate

from ..client_user_presence_base import ClientUserPBase
from ..preinstanced import Status


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
        Activity('orin dance', activity_id = 202302080000, activity_type = ActivityType.game),
        Activity('okuu dance', activity_id = 202302080001, activity_type = ActivityType.game),
    ]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase()
    
    data = {
        'activities': [activity.to_data(defaults = True, include_internals = True) for activity in activities],
        'status': status.value,
        'client_status': statuses.copy(),
    }
    
    user._update_presence(data)
    
    vampytest.assert_eq(user.activities, activities)
    vampytest.assert_is(user.status, status)
    vampytest.assert_eq(user.statuses, statuses)
    


def test__ClientUserPBase__difference_update_presence():
    """
    Tests whether ``ClientUserPBase._difference_update_presence`` works as intended.
    """
    old_activities = [
        Activity('orin dance', activity_id = 202302080002, activity_type = ActivityType.game),
        Activity('okuu dance', activity_id = 202302080003, activity_type = ActivityType.game),
    ]
    old_status = Status.online
    old_statuses = {'mobile': Status.online.value}
    
    new_activities = [
        Activity('okuu lay', activity_id = 202302080003, activity_type = ActivityType.game),
        Activity('satori dance', activity_id = 202302080004, activity_type = ActivityType.game),
    ]
    new_status = Status.idle
    new_statuses = {'desktop': Status.online.value}
    
    user = ClientUserPBase(
        activities = old_activities,
        status = old_status,
        statuses = old_statuses.copy(),
    )
    
    data = {
        'activities': [activity.to_data(defaults = True, include_internals = True) for activity in new_activities],
        'status': new_status.value,
        'client_status': new_statuses.copy(),
    }
    
    expected_output = {
        'activities': ActivityChange(
            added = [Activity('satori dance', activity_id = 202302080004, activity_type = ActivityType.game)],
            removed = [Activity('orin dance', activity_id = 202302080002, activity_type = ActivityType.game)],
            updated = [
                ActivityUpdate(
                    activity = Activity('okuu lay', activity_id = 202302080003, activity_type = ActivityType.game),
                    old_attributes = {'name': 'okuu dance'}
                ),
            ],
        ),
        'status': old_status,
        'statuses': old_statuses,
    }
    
    output = user._difference_update_presence(data)
    
    vampytest.assert_eq(output, expected_output)
    
    vampytest.assert_eq(user.activities, new_activities)
    vampytest.assert_is(user.status, new_status)
    vampytest.assert_eq(user.statuses, new_statuses)
    
