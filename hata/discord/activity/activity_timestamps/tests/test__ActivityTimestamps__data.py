from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..timestamps import ActivityTimestamps

from .test__ActivityTimestamps__constructor import _assert_fields_set


def test__ActivityTimestamps__from_data__0():
    """
    Tests whether ``ActivityTimestamps.from_data`` works as intended.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42)
    start = DateTime(2016, 5, 2, 15, 10, 34)
    
    data = {
        'end': datetime_to_millisecond_unix_time(end),
        'start': datetime_to_millisecond_unix_time(start),
    }
    field = ActivityTimestamps.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.end, end)
    vampytest.assert_eq(field.start, start)


def test__ActivityTimestamps__to_data__0():
    """
    Tests whether ``ActivityTimestamps.to_data`` works as intended.
    
    Case: Include defaults.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42)
    start = DateTime(2016, 5, 2, 15, 10, 34)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    
    expected_output = {
        'end': datetime_to_millisecond_unix_time(end),
        'start': datetime_to_millisecond_unix_time(start),
    }
    
    vampytest.assert_eq(
        field.to_data(defaults = True),
        expected_output,
    )
