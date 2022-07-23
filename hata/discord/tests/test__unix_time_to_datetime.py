from datetime import datetime as DateTime

import vampytest

from .. import unix_time_to_datetime


def test__unix_time_to_datetime__0():
    """
    Issue: `unix_time_to_datetime` returned bad value.
    """
    unix_time = 1464100062
    date_time = DateTime(2016, 5, 24, 14, 27, 42)
    
    vampytest.assert_eq(unix_time_to_datetime(unix_time), date_time)
