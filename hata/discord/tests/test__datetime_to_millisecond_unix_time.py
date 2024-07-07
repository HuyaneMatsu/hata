from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..utils import datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime


def test_datetime_to_millisecond_unix_time():
    """
    Tests whether ``datetime_to_millisecond_unix_time`` works as intended by round converting a date time.
    """
    date_time = DateTime(2016, 5, 24, 14, 27, 42, tzinfo = TimeZone.utc)
    
    converted = millisecond_unix_time_to_datetime(datetime_to_millisecond_unix_time(date_time))
    
    vampytest.assert_eq(date_time, converted)
