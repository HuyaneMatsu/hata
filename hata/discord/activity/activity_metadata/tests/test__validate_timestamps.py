from datetime import datetime as DateTime

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import validate_timestamps


def test__validate_timestamps__0():
    """
    Tests whether `validate_timestamps` works as intended.
    
    Case: passing.
    """
    timestamps = ActivityTimestamps(start = DateTime(2016, 3, 16))
    
    for input_value, expected_output in (
        (None, None),
        (timestamps, timestamps),
    ):
        output = validate_timestamps(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_timestamps__1():
    """
    Tests whether `validate_timestamps` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_timestamps(input_value)
