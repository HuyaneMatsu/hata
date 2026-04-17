import vampytest

from ....activity import Activity

from ...activity_update import ActivityUpdate

from ..activity_change import ActivityChange

from .test__ActivityChange__constructor import _assert_fields_set


def test__ActivityChange__copy():
    """
    Tests whether ``ActivityChange.copy`` works as intended.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = activity_change.copy()
    _assert_fields_set(activity_change)
    vampytest.assert_is_not(activity_change, copy)
    vampytest.assert_eq(activity_change, copy)


def test__ActivityChange__copy_with__no_fields():
    """
    Tests whether ``ActivityChange.copy_with`` works as intended.
    
    Case: No fields given.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = activity_change.copy_with()
    _assert_fields_set(activity_change)
    vampytest.assert_is_not(activity_change, copy)
    vampytest.assert_eq(activity_change, copy)



def test__ActivityChange__copy_with__all_fields():
    """
    Tests whether ``ActivityChange.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_added = [Activity('hello')]
    old_updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    old_removed = [Activity('innit')]
    new_added = [Activity('hell')]
    new_updated = [ActivityUpdate(old_attributes = {'b': 'c'})]
    new_removed = [Activity('yall')]
    
    activity_change = ActivityChange(
        added = old_added,
        updated = old_updated,
        removed = old_removed,
    )
    
    copy = activity_change.copy_with(
        added = new_added,
        updated = new_updated,
        removed = new_removed,
    )
    
    _assert_fields_set(activity_change)
    vampytest.assert_is_not(activity_change, copy)

    vampytest.assert_eq(copy.added, new_added)
    vampytest.assert_eq(copy.updated, new_updated)
    vampytest.assert_eq(copy.removed, new_removed)



def _iter_options__iter_added():
    activity_0 = Activity('hello')
    activity_1 = Activity('hell')
    
    yield None, []
    yield [activity_0], [activity_0]
    yield [activity_0, activity_1], [activity_0, activity_1]


@vampytest._(vampytest.call_from(_iter_options__iter_added()).returning_last())
def test__ActivityChange__iter_added(input_value):
    """
    Tests whether ``ActivityChange.iter_added`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Activity>`
        Added activities to test with.
    
    Returns
    -------
    output : `list<Activity>
    """
    activity_change = ActivityChange(
        added = input_value,
    )
    
    return [*activity_change.iter_added()]


def _iter_options__iter_removed():
    activity_0 = Activity('hello')
    activity_1 = Activity('hell')
    
    yield None, []
    yield [activity_0], [activity_0]
    yield [activity_0, activity_1], [activity_0, activity_1]


@vampytest._(vampytest.call_from(_iter_options__iter_removed()).returning_last())
def test__ActivityChange__iter_removed(input_value):
    """
    Tests whether ``ActivityChange.iter_removed`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Activity>`
        Added activities to test with.
    
    Returns
    -------
    output : `list<Activity>
    """
    activity_change = ActivityChange(
        removed = input_value,
    )
    
    return [*activity_change.iter_removed()]


def _iter_options__iter_updated():
    activity_update_0 = ActivityUpdate(activity = Activity('hello'))
    activity_update_1 = ActivityUpdate(activity = Activity('hell'))

    yield None, []
    yield [activity_update_0], [activity_update_0]
    yield [activity_update_0, activity_update_1], [activity_update_0, activity_update_1]


@vampytest._(vampytest.call_from(_iter_options__iter_updated()).returning_last())
def test__ActivityChange__iter_updated(input_value):
    """
    Tests whether ``ActivityChange.iter_updated`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ActivityUpdate>`
        Added activities to test with.
    
    Returns
    -------
    output : `list<ActivityUpdate>
    """
    activity_change = ActivityChange(
        updated = input_value,
    )
    
    return [*activity_change.iter_updated()]
