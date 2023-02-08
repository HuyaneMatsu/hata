import vampytest

from ....activity import Activity, ActivityType

from ..client_user_presence_base import ClientUserPBase
from ..preinstanced import Status


def test__ClientUserPBase__activity__0():
    """
    Tests whether ``ClientUserPBase.activity`` works as intended.
    
    Case: Has activities.
    """
    activities = [
        Activity(state = 'orin dance', activity_type = ActivityType.custom),
        Activity('orin dance', activity_type = ActivityType.competing),
        Activity('orin dance', activity_type = ActivityType.game),
    ]
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.activity
    vampytest.assert_is(output, activities[1])


def test__ClientUserPBase__activity__1():
    """
    Tests whether ``ClientUserPBase.activity`` works as intended.
    
    Case: No activities.
    """
    activities = []
    
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.activity
    vampytest.assert_is(output, None)



def test__ClientUserPBase__activity__2():
    """
    Tests whether ``ClientUserPBase.activity`` works as intended.
    
    Case: Only custom activity.
    """
    activities = [
        Activity(state = 'orin dance', activity_type = ActivityType.custom),
    ]
    
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.activity
    vampytest.assert_is(output, None)



def test__ClientUserPBase__custom_activity__0():
    """
    Tests whether ``ClientUserPBase.custom_activity`` works as intended.
    
    Case: Has activities.
    """
    activities = [
        Activity('orin dance', activity_type = ActivityType.competing),
        Activity(state = 'orin dance', activity_type = ActivityType.custom),
        Activity('orin dance', activity_type = ActivityType.game),
    ]
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.custom_activity
    vampytest.assert_is(output, activities[1])


def test__ClientUserPBase__custom_activity__1():
    """
    Tests whether ``ClientUserPBase.custom_activity`` works as intended.
    
    Case: No activities.
    """
    activities = []
    
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.custom_activity
    vampytest.assert_is(output, None)


def test__ClientUserPBase__custom_activity__2():
    """
    Tests whether ``ClientUserPBase.custom_activity`` works as intended.
    
    Case: No custom activity.
    """
    activities = [
        Activity('orin dance', activity_type = ActivityType.game),
    ]
    
    user = ClientUserPBase(
        activities = activities,
    )
    
    output = user.custom_activity
    vampytest.assert_is(output, None)


def test__ClientUserPBase__platform__0():
    """
    Tests whether ``ClientUserPBase.platform`` works as intended.
    
    Case: Has status.
    """
    status = Status.idle
    statuses = {
        'desktop': Status.dnd.value,
        'mobile': Status.idle.value,
    }
    
    user = ClientUserPBase(
        status = status,
        statuses = statuses,
    )
    
    output = user.platform
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, 'mobile')


def test__ClientUserPBase__platform__1():
    """
    Tests whether ``ClientUserPBase.platform`` works as intended.
    
    Case: No status.
    """
    user = ClientUserPBase()
    
    output = user.platform
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')
