from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import User

from ..scheduled_event_user_entry import ScheduledEventUserEntry

from .test__ScheduledEventUserEntry__constructor import _assert_fields_set


def test__ScheduledEventUserEntry__copy():
    """
    Tests whether ``ScheduledEventUserEntry.copy`` works as intended.
    """
    scheduled_event_id = 202602100050
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100051,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    
    copy = scheduled_event_user_entry.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_entry)


def test__ScheduledEventUserEntry__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventUserEntry.copy_with`` works as intended.
    
    Case: no fields given.
    """
    scheduled_event_id = 202602100052
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100053,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    
    copy = scheduled_event_user_entry.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_entry)


def test__ScheduledEventUserEntry__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventUserEntry.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_scheduled_event_id = 202602100054
    old_timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_user = User.precreate(
        202602100055,
        name = 'Suwako',
    )
    
    new_scheduled_event_id = 202602100056
    new_timestamp = DateTime(2016, 5, 24, tzinfo = TimeZone.utc)
    new_user = User.precreate(
        202602100057,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = old_scheduled_event_id,
        timestamp = old_timestamp,
        user = old_user,
    )
    
    copy = scheduled_event_user_entry.copy_with(
        scheduled_event_id = new_scheduled_event_id,
        timestamp = new_timestamp,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_entry)

    vampytest.assert_eq(copy.scheduled_event_id, new_scheduled_event_id)
    vampytest.assert_eq(copy.timestamp, new_timestamp)
    vampytest.assert_is(copy.user, new_user)
