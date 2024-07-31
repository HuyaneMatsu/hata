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
        Activity('orin dance', activity_type = ActivityType.playing),
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
        Activity('orin dance', activity_type = ActivityType.playing),
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
        Activity('orin dance', activity_type = ActivityType.playing),
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



def test__ClientUserPBase__get_status_by_platform__0():
    """
    Tests whether ``ClientUserPBase.get_status_by_platform`` works as intended.
    
    Case: No status.
    """
    user = ClientUserPBase()
    
    output = user.get_status_by_platform('')
    
    vampytest.assert_instance(output, Status)
    vampytest.assert_is(output, Status.offline)


def test__ClientUserPBase__get_status_by_platform__1():
    """
    Tests whether ``ClientUserPBase.get_status_by_platform`` works as intended.
    
    Case: Other platform.
    """
    statuses = {
        'desktop': Status.dnd.value,
        'mobile': Status.idle.value,
    }
    
    user = ClientUserPBase(
        statuses = statuses,
    )
    
    output = user.get_status_by_platform('web')
    
    vampytest.assert_instance(output, Status)
    vampytest.assert_is(output, Status.offline)


def test__ClientUserPBase__get_status_by_platform__2():
    """
    Tests whether ``ClientUserPBase.get_status_by_platform`` works as intended.
    
    Case: Hit with platform.
    """
    desktop_status = Status.dnd
    
    statuses = {
        'desktop': desktop_status.value,
        'mobile': Status.idle.value,
    }
    
    user = ClientUserPBase(
        statuses = statuses,
    )
    
    output = user.get_status_by_platform('desktop')
    
    vampytest.assert_instance(output, Status)
    vampytest.assert_is(output, desktop_status)
