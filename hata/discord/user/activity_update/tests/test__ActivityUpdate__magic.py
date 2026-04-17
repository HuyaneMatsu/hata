import vampytest

from ....activity import Activity

from ..activity_update import ActivityUpdate


def test__ActivityUpdate__repr():
    """
    Tests whether ``ActivityUpdate.__repr__`` works as intended.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(repr(activity_update), str)


def test__ActivityUpdate__hash():
    """
    Tests whether ``ActivityUpdate.__hash__`` works as intended.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(hash(activity_update), int)


def test__ActivityUpdate__eq():
    """
    Tests whether ``ActivityUpdate.__eq__`` works as intended.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    keyword_parameters = {    
        'activity': activity,
        'old_attributes': old_attributes,
    }
    
    activity_update = ActivityUpdate(**keyword_parameters)
    vampytest.assert_eq(activity_update, activity_update)
    vampytest.assert_ne(activity_update, object())
    
    for field_name, field_value in (
        ('activity',  Activity('hell')),
        ('old_attributes', {'everyone': 'lies'}),
    ):
        test_activity_update = ActivityUpdate(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(activity_update, test_activity_update)


def test__ActivityUpdate__unpack():
    """
    Tests whether ``ActivityUpdate`` unpacking works as intended.
    """
    activity = Activity('hello')
    old_attributes = {'a': 'b'}
    
    activity_update = ActivityUpdate(
        activity = activity,
        old_attributes = old_attributes,
    )
    
    unpacked = [*activity_update]
    vampytest.assert_eq(len(unpacked), len(activity_update))
