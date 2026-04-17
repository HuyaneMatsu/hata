from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..timestamps import ActivityTimestamps


def test__ActivityTimestamps__repr():
    """
    Tests whether ``ActivityTimestamps.__repr__`` works as intended.
    """
    field = ActivityTimestamps(
        end = DateTime(2016, 5, 24, 14, 27, 42, tzinfo = TimeZone.utc),
        start = DateTime(2016, 5, 2, 15, 10, 34, tzinfo = TimeZone.utc),
    )
    
    vampytest.assert_instance(repr(field), str)


def test__ActivityTimestamps__eq():
    """
    Tests whether ``ActivityTimestamps.__repr__`` works as intended.
    """
    fields = {
        'end': DateTime(2016, 5, 24, 14, 27, 42, tzinfo = TimeZone.utc),
        'start': DateTime(2016, 5, 2, 15, 10, 34, tzinfo = TimeZone.utc),
    }
    
    field_original = ActivityTimestamps(**fields)
    
    vampytest.assert_eq(field_original, field_original)
    
    for field_name in (
        'end',
        'start',
    ):
        field_altered = ActivityTimestamps(**{**fields, field_name: None})
        vampytest.assert_ne(field_original, field_altered)


def test__ActivityTimestamps__hash():
    """
    Tests whether ``ActivityTimestamps.__hash__`` works as intended.
    """
    field = ActivityTimestamps(
        end =  DateTime(2016, 5, 24, 14, 27, 42, tzinfo = TimeZone.utc),
        start = DateTime(2016, 5, 2, 15, 10, 34, tzinfo = TimeZone.utc),
    )
    
    vampytest.assert_instance(hash(field), int)


def test__ActivityTimestamps__bool():
    """
    Tests whether ``ActivityTimestamps.__bool__`` works as intended.
    """
    field = ActivityTimestamps()
    
    field_bool = bool(field)
    vampytest.assert_instance(field_bool, bool)
    vampytest.assert_false(field_bool)
    
    date_time = DateTime(2016, 5, 2, 15, 10, 34, tzinfo = TimeZone.utc)
    
    for field_name in (
        'end',
        'start',
    ):
        field = ActivityTimestamps(**{field_name: date_time})
        
        field_bool = bool(field)
        vampytest.assert_instance(field_bool, bool)
        vampytest.assert_true(field_bool)
