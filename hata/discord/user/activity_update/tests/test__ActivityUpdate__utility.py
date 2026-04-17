import vampytest

from ....activity import Activity

from ..activity_update import ActivityUpdate

from .test__ActivityUpdate__constructor import _assert_fields_set


def test__ActivityUpdate__copy():
    """
    Tests whether ``ActivityUpdate.copy`` works as intended.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    
    copy = activity_update.copy()
    _assert_fields_set(activity_update)
    vampytest.assert_is_not(activity_update, copy)
    vampytest.assert_eq(activity_update, copy)


def test__ActivityUpdate__copy_with__0():
    """
    Tests whether ``ActivityUpdate.copy_with`` works as intended.
    
    Case: No fields given.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    
    copy = activity_update.copy_with()
    _assert_fields_set(activity_update)
    vampytest.assert_is_not(activity_update, copy)
    vampytest.assert_eq(activity_update, copy)



def test__ActivityUpdate__copy_with__1():
    """
    Tests whether ``ActivityUpdate.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_activity = Activity('hello')
    old_old_attributes = {'a': 'b'}
    new_activity = Activity('hell')
    new_old_attributes = {'b': 'c'}
    
    activity_update = ActivityUpdate(
        activity = old_activity,
        old_attributes = old_old_attributes,
    )
    
    copy = activity_update.copy_with(
        activity = new_activity,
        old_attributes = new_old_attributes,
    )
    
    _assert_fields_set(activity_update)
    vampytest.assert_is_not(activity_update, copy)

    vampytest.assert_eq(copy.activity, new_activity)
    vampytest.assert_eq(copy.old_attributes, new_old_attributes)
