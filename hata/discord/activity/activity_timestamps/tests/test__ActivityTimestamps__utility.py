from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..timestamps import ActivityTimestamps

from .test__ActivityTimestamps__constructor import _assert_fields_set


def test__ActivityTimestamps__copy():
    """
    Tests whether ``ActivityTimestamps.copy`` works as intended.
    """
    end = DateTime(2016, 1, 14, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    
    copy = field.copy()
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(field, copy)


def test__ActivityTimestamps__copy_with__0():
    """
    Tests whether ``ActivityTimestamps.copy_with`` works as intended.
    
    Case: No fields given.
    """
    end = DateTime(2016, 1, 14, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    
    copy = field.copy_with()
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(field, copy)


def test__ActivityTimestamps__copy_with__1():
    """
    Tests whether ``ActivityTimestamps.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_end = DateTime(2016, 1, 14, tzinfo = TimeZone.utc)
    old_start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    new_end = DateTime(2016, 1, 12, tzinfo = TimeZone.utc)
    new_start = DateTime(2016, 1, 12, tzinfo = TimeZone.utc)
    
    field = ActivityTimestamps(
        end = old_end,
        start = old_start,
    )
    
    copy = field.copy_with(
        end = new_end,
        start = new_start,
    )
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(copy.end, new_end)
    vampytest.assert_eq(copy.start, new_start)
