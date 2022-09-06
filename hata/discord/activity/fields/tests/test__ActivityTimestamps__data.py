from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from .. import ActivityTimestamps


def test__ActivityTimestamps__from_data__0():
    """
    Tests whether ``ActivityTimestamps.from_data`` works as intended.
    
    Case: all fields given.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42)
    start = DateTime(2016, 5, 2, 15, 10, 34)
    
    field = ActivityTimestamps.from_data({
        'end': datetime_to_millisecond_unix_time(end),
        'start': datetime_to_millisecond_unix_time(start),
    })
    
    vampytest.assert_eq(field.end, end)
    vampytest.assert_eq(field.start, start)


def test__ActivityTimestamps__from_data__1():
    """
    Tests whether ``ActivityTimestamps.from_data`` works as intended.
    
    Case: no fields given.
    """
    field = ActivityTimestamps.from_data({})
    
    vampytest.assert_is(field.end, None)
    vampytest.assert_is(field.start, None)


def test__ActivityTimestamps__to_data__0():
    """
    Tests whether ``ActivityTimestamps.to_data`` works as intended.
    
    Case: all fields set.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42)
    start = DateTime(2016, 5, 2, 15, 10, 34)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    
    data = field.to_data()
    
    vampytest.assert_in('end', data)
    vampytest.assert_in('start', data)
    
    vampytest.assert_eq(data['end'], datetime_to_millisecond_unix_time(end))
    vampytest.assert_eq(data['start'], datetime_to_millisecond_unix_time(start))


def test__ActivityTimestamps__to_data__1():
    """
    Tests whether ``ActivityTimestamps.to_data`` works as intended.
    
    Case: no fields set.
    """
    field = ActivityTimestamps()
    data = field.to_data()
    
    vampytest.assert_not_in('end', data)
    vampytest.assert_not_in('start', data)
