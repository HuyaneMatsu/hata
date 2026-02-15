from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import ClientUserBase, User

from ..scheduled_event_user_entry import ScheduledEventUserEntry


def _assert_fields_set(scheduled_event_user_entry):
    """
    Asserts whether all fields are of the given instance.
    
    Parameters
    ----------
    scheduled_event_user_entry : ``ScheduledEventUserEntry``
        The instance to check.
    """
    vampytest.assert_instance(scheduled_event_user_entry, ScheduledEventUserEntry)
    vampytest.assert_instance(scheduled_event_user_entry.scheduled_event_id, int)
    vampytest.assert_instance(scheduled_event_user_entry.timestamp, DateTime, nullable = True)
    vampytest.assert_instance(scheduled_event_user_entry.user, ClientUserBase)


def test__ScheduledEventUserEntry__new__no_fields():
    """
    Tests whether ``ScheduledEventUserEntry.__new__`` works as intended.
    
    Case: no fields given.
    """
    scheduled_event_user_entry = ScheduledEventUserEntry()
    _assert_fields_set(scheduled_event_user_entry)


def test__ScheduledEventUserEntry__new__all_fields():
    """
    Tests whether ``ScheduledEventUserEntry.__new__`` works as intended.
    
    Case: all fields given.
    """
    scheduled_event_id = 202602100020
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100021,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    _assert_fields_set(scheduled_event_user_entry)
    
    vampytest.assert_eq(scheduled_event_user_entry.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(scheduled_event_user_entry.timestamp, timestamp)
    vampytest.assert_is(scheduled_event_user_entry.user, user)
