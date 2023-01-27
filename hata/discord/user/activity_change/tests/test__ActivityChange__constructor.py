import vampytest

from ....activity import Activity

from ...activity_update import ActivityUpdate

from ..activity_change import ActivityChange


def _assert_fields_set(activity_change):
    """
    Tests whether all fields are set of the given activity change.
    
    Parameters
    ----------
    activity_change : ``ActivityChange``
        The activity change to check.
    """
    vampytest.assert_instance(activity_change, ActivityChange)
    vampytest.assert_instance(activity_change.added, list, nullable = True)
    vampytest.assert_instance(activity_change.updated, list, nullable = True)
    vampytest.assert_instance(activity_change.removed, list, nullable = True)


def test__ActivityChange__new__0():
    """
    Tests whether ``ActivityChange.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_change = ActivityChange()
    _assert_fields_set(activity_change)


def test__ActivityChange__new__1():
    """
    Tests whether ``ActivityChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    _assert_fields_set(activity_change)

    vampytest.assert_eq(activity_change.added, added)
    vampytest.assert_eq(activity_change.updated, updated)
    vampytest.assert_eq(activity_change.removed, removed)


def test__ActivityChange__from_fields():
    """
    Tests whether ``ActivityChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange.from_fields(added, updated, removed)
    _assert_fields_set(activity_change)

    vampytest.assert_eq(activity_change.added, added)
    vampytest.assert_eq(activity_change.updated, updated)
    vampytest.assert_eq(activity_change.removed, removed)
