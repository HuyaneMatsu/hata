from datetime import datetime as DateTime

import vampytest

from .. import datetime_to_unix_time


def test_datetime_to_unix_time__0():
    """
    Tests whether ``datetime_to_unix_time`` returns the correct value.
    """
    unix_time = 1464100062
    date_time = DateTime(2016, 5, 24, 14, 27, 42)
    
    vampytest.assert_eq(datetime_to_unix_time(date_time), unix_time)
