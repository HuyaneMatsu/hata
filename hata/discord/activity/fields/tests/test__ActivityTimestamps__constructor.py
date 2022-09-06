from datetime import datetime as DateTime

import vampytest

from .. import ActivityTimestamps


def test__ActivityTimestamps__new__0():
    """
    Tests whether ``ActivityTimestamps.__new__`` sets values as expected.
    """
    end = DateTime(2016, 5, 24, 14, 27, 42)
    start = DateTime(2016, 5, 2, 15, 10, 34)
    
    field = ActivityTimestamps(
        end = end,
        start = start,
    )
    
    vampytest.assert_eq(field.end, end)
    vampytest.assert_eq(field.start, start)
