import vampytest

from ....activity import Activity

from ...activity_update import ActivityUpdate

from ..activity_change import ActivityChange


def test__ActivityChange__repr():
    """
    Tests whether ``ActivityChange.__repr__`` works as intended.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(repr(activity_change), str)


def test__ActivityChange__hash():
    """
    Tests whether ``ActivityChange.__hash__`` works as intended.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(hash(activity_change), int)


def test__ActivityChange__eq():
    """
    Tests whether ``ActivityChange.__eq__`` works as intended.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    keyword_parameters = {    
        'added': added,
        'updated': updated,
        'removed': removed,
    }
    
    activity_change = ActivityChange(**keyword_parameters)
    vampytest.assert_eq(activity_change, activity_change)
    vampytest.assert_ne(activity_change, object())
    
    for field_name, field_value in (
        ('added',  None),
        ('updated', None),
        ('removed', None),
    ):
        test_activity_change = ActivityChange(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(activity_change, test_activity_change)


def test__ActivityChange__unpack():
    """
    Tests whether ``ActivityChange`` unpacking works as intended.
    """
    added = [Activity('hello')]
    updated = [ActivityUpdate(old_attributes = {'a': 'b'})]
    removed = [Activity('innit')]
    
    activity_change = ActivityChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    unpacked = [*activity_change]
    vampytest.assert_eq(len(unpacked), len(activity_change))
