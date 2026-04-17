import vampytest

from ....activity import Activity

from ..activity_update import ActivityUpdate


def _assert_fields_set(activity_update):
    """
    Tests whether all fields are set of the given activity update.
    
    Parameters
    ----------
    activity_update : ``ActivityUpdate``
        The activity update to check.
    """
    vampytest.assert_instance(activity_update, ActivityUpdate)
    vampytest.assert_instance(activity_update.activity, Activity)
    vampytest.assert_instance(activity_update.old_attributes, dict)


def test__ActivityUpdate__new__0():
    """
    Tests whether ``ActivityUpdate.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_update = ActivityUpdate()
    _assert_fields_set(activity_update)


def test__ActivityUpdate__new__1():
    """
    Tests whether ``ActivityUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    _assert_fields_set(activity_update)

    vampytest.assert_eq(activity_update.activity, activity)
    vampytest.assert_eq(activity_update.old_attributes, old_attributes)


def test__ActivityUpdate__from_fields():
    """
    Tests whether ``ActivityUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate.from_fields(activity, old_attributes)
    _assert_fields_set(activity_update)

    vampytest.assert_eq(activity_update.activity, activity)
    vampytest.assert_eq(activity_update.old_attributes, old_attributes)
