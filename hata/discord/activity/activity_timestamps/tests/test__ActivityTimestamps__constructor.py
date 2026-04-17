from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..timestamps import ActivityTimestamps


def _assert_fields_set(field):
    """
    Asserts whether every fields are set of the given activity timestamps.
    
    Parameters
    ----------
    field : ``ActivityTimestamps``
        The activity timestamp field to check.
    """
    vampytest.assert_instance(field, ActivityTimestamps)
    vampytest.assert_instance(field.end, DateTime, nullable = True)
    vampytest.assert_instance(field.start, DateTime, nullable = True)


def test__ActivityTimestamps__new__0():
    """
    Tests whether ``ActivityTimestamps.__new__`` works as intended.
    
    Case: No fields given.
    """
    field = ActivityTimestamps()
    _assert_fields_set(field)


def test__ActivityTimestamps__new__1():
    """
    Tests whether ``ActivityTimestamps.__new__`` works as intended.
    
    Case: All fields given.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 2, 15, 10, 34, tzinfo = TimeZone.utc)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.end, end)
    vampytest.assert_eq(field.start, start)
